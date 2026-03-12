from faster_whisper import WhisperModel
from pynvml import (
    nvmlInit,
    nvmlShutdown,
    nvmlDeviceGetCount,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetName,
)


class Audio_to_text:
    def __init__(self, model_size: str = "small"):
        device, device_index, compute_type = self._select_backend()

        try:
            print(
                f"[AUDIO] Loading WhisperModel(model_size={model_size}, "
                f"device={device}, device_index={device_index}, compute_type={compute_type})"
            )
            self.model = WhisperModel(
                model_size_or_path=model_size,
                device=device,
                device_index=device_index,
                compute_type=compute_type,
            )
            self.device = device
            self.device_index = device_index
            self.compute_type = compute_type

        except Exception as e:
            print(f"[AUDIO] CUDA load failed, falling back to CPU. Error: {e}")
            self.model = WhisperModel(
                model_size_or_path=model_size,
                device="cpu",
                compute_type="int8",
            )
            self.device = "cpu"
            self.device_index = 0
            self.compute_type = "int8"

    def transcribe(self, audio_file: str) -> str:
        print(
            f"[AUDIO] Transcribing file={audio_file} "
            f"with device={self.device}, device_index={self.device_index}, compute_type={self.compute_type}"
        )
        segments, info = self.model.transcribe(audio_file)

        text = []
        for segment in segments:
            text.append(segment.text.strip())

        return " ".join(t for t in text if t)

    def _select_backend(self) -> tuple[str, int, str]:
        """
        Returns:
            (device, device_index, compute_type)
        """
        try:
            nvmlInit()
            count = nvmlDeviceGetCount()

            if count <= 0:
                return "cpu", 0, "int8"

            best_index = None
            best_free_mem = -1

            for i in range(count):
                handle = nvmlDeviceGetHandleByIndex(i)
                mem = nvmlDeviceGetMemoryInfo(handle)
                name = nvmlDeviceGetName(handle)
                gpu_name = name.decode() if isinstance(name, bytes) else str(name)

                print(
                    f"[AUDIO] GPU {i}: name={gpu_name}, "
                    f"free_vram_mb={mem.free / (1024 * 1024):.0f}"
                )

                if mem.free > best_free_mem:
                    best_free_mem = mem.free
                    best_index = i

            nvmlShutdown()

            if best_index is not None:
                return "cuda", best_index, "float16"

        except Exception as e:
            print(f"[AUDIO] GPU detection failed. Falling back to CPU. Error: {e}")

        return "cpu", 0, "int8"