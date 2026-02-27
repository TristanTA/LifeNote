from faster_whisper import WhisperModel
from pynvml import *  # noqa: F401,F403
import os
import ffmpeg
import tempfile
import uuid
import shutil

WHISPER_PROFILES = {
    "cpu": {"model": "base", "device": "cpu", "compute_type": "int8"},
    "cuda_float16": {"model": "medium", "device": "cuda", "compute_type": "float16"},
    "cuda_int8": {"model": "small", "device": "cuda", "compute_type": "int8_float16"},
}


class AudioReader:
    """Wrapper around Faster-Whisper with optional GPU profile detection."""

    def __init__(self, debug: bool = False, maunal_profile: dict | bool = False):
        """Initialize the transcription model.

        Args:
            debug:
                If True, prints minimal [DEBUG] logs.
            maunal_profile:
                - False: auto-select a profile using GPU detection (or CPU fallback).
                - dict: use a manual profile:
                    {
                      "model": "base" | "small" | "medium",
                      "device": "cpu" | "cuda",
                      "compute_type": "int8" | "float16" | "int8_float16"
                    }

        Use:
            model = AudioReader()
            transcript, metadata = model.transcribe(audio_file)
        """
        self.profile = {}
        self.debug = debug

        if not maunal_profile:
            profile_key = self.get_user_profile()        # "cpu" | "cuda_int8" | "cuda_float16"
            self.profile = WHISPER_PROFILES[profile_key] # dict with model/device/compute_type
        else:
            self.profile["model"] = maunal_profile["model"]
            self.profile["device"] = maunal_profile["device"]
            self.profile["compute_type"] = maunal_profile["compute_type"]
            profile_key = "Manual"

        if self.debug:
            print(f"[DEBUG] Profile key: {profile_key}")
            print(f"[DEBUG] Profile: {self.profile}")

        self.model = WhisperModel(
            self.profile["model"],
            device=self.profile["device"],
            compute_type=self.profile["compute_type"],
            cpu_threads=os.cpu_count() or 4,
            num_workers=1,
        )

        if self.debug:
            print("[DEBUG] Model initialized")

    def get_user_profile(self) -> str:
        """Choose a whisper profile using basic GPU VRAM heuristics (best GPU by VRAM)."""
        gpu_info = self.detect_nvidia_gpu()

        if self.debug:
            print(f"[DEBUG] GPU found: {gpu_info.get('gpu_found')}")

        if not gpu_info.get("gpu_found"):
            return "cpu"

        gpus = gpu_info.get("gpus", [])
        if not gpus:
            return "cpu"

        # Pick the GPU with the most VRAM.
        best_gpu = max(gpus, key=lambda g: g.get("total_vram_gb", 0) or 0)
        vram = best_gpu.get("total_vram_gb", 0) or 0

        if self.debug:
            name = best_gpu.get("name", "unknown")
            idx = best_gpu.get("index", "unknown")
            print(f"[DEBUG] Best GPU: index={idx}, name={name}, vram_gb={vram}")
            print(f"[DEBUG] All GPUs: {[{'index': g.get('index'), 'name': g.get('name'), 'vram_gb': g.get('total_vram_gb')} for g in gpus]}")

        if vram >= 8:
            return "cuda_float16"
        elif vram >= 4:
            return "cuda_int8"
        return "cpu"

    def detect_nvidia_gpu(self) -> dict:
        """Detect NVIDIA GPUs and VRAM via NVML (best-effort)."""
        try:
            nvmlInit()
            device_count = nvmlDeviceGetCount()

            if self.debug:
                print(f"[DEBUG] NVML device_count={device_count}")

            if device_count == 0:
                return {"gpu_found": False, "gpus": []}

            gpus = []
            for i in range(device_count):
                handle = nvmlDeviceGetHandleByIndex(i)
                name = self._nvml_to_str(nvmlDeviceGetName(handle))
                mem = nvmlDeviceGetMemoryInfo(handle)
                gpus.append(
                    {
                        "index": i,
                        "name": name,
                        "total_vram_gb": round(mem.total / (1024**3), 2),
                        "free_vram_gb": round(mem.free / (1024**3), 2),
                        "used_vram_gb": round(mem.used / (1024**3), 2),
                    }
                )

            driver = name = self._nvml_to_str(nvmlDeviceGetName(handle))
            return {"gpu_found": True, "driver_version": driver, "gpus": gpus}

        except Exception as e:
            if self.debug:
                print(f"[DEBUG] NVML error: {type(e).__name__}: {e}")
            return {"gpu_found": False, "gpus": [], "error": f"{type(e).__name__}: {e}"}

        finally:
            try:
                nvmlShutdown()
            except Exception:
                pass

    def transcribe(self, audio_file):
        """Transcribe an audio file to text.

        Args:
            audio_file: Path to an audio file.

        Returns:
            (transcript_text, info)
        """
        if self.debug:
            print(f"[DEBUG] Transcribing message {audio_file}...")

        clean_audio_file = self.prepare_audio(audio_file)

        if self.debug and clean_audio_file != os.path.abspath(audio_file):
            print(f"[DEBUG] Using cleaned audio: {clean_audio_file}")

        segments, info = self.model.transcribe(clean_audio_file)

        segment_package = ""
        for segment in segments:
            segment_package += segment.text

        if self.debug:
            print("[DEBUG] Message transcribed")

        return segment_package, info

    def prepare_audio(self, input_path: str) -> str:
        """Normalize audio into WAV 16kHz mono 16-bit PCM (when ffmpeg is available).

        Args:
            input_path: Path to the source audio file.

        Returns:
            Path to a cleaned WAV file. If ffmpeg is missing and the input is already a WAV,
            returns the original path. Otherwise raises FileNotFoundError.
        """
        input_path = os.path.abspath(input_path)

        if self.debug:
            print(f"[DEBUG] prepare_audio(): input_path={input_path}")

        ffmpeg_path = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
        if not ffmpeg_path:
            if self.debug:
                print("[DEBUG] prepare_audio(): ffmpeg not found")

            # If it's already wav, just use it.
            if input_path.lower().endswith(".wav"):
                return input_path

            raise FileNotFoundError(
                "ffmpeg executable not found. Install ffmpeg or provide a .wav file."
            )

        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"whisper_clean_{uuid.uuid4().hex}.wav")

        if self.debug:
            print(f"[DEBUG] prepare_audio(): output_path={output_path}")

        (
            ffmpeg.input(input_path)
            .output(output_path, ac=1, ar=16000, format="wav", acodec="pcm_s16le")
            .overwrite_output()
            .run(quiet=True)
        )

        return output_path

    def _nvml_to_str(self, v) -> str:
        """NVML may return bytes or str depending on pynvml version; normalize to str."""
        if isinstance(v, bytes):
            return v.decode(errors="ignore")
        return str(v)