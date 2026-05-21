"""CosyVoice API service for voice cloning and synthesis."""
import os
from typing import Optional

# dashscope 只在运行时导入，不在模块加载时
try:
    from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False


class CosyVoiceService:
    """Alibaba Cloud CosyVoice API service."""
    
    # 可用的系统音色列表
    VOICES = {
        "longanyang": "龙傲炎",
        "xiaoxian": "小贤",
        "nvpuhong": "女浦东",
        "longjiang": "龙江",
        "xiaomei": "小美",
        "xiaojun": "小君",
        "aigen": "艾根",
        "aijia": "艾嘉",
        "aicheck": "艾克",
        "aiming": "艾明",
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
    
    def _init_dashscope(self):
        """Lazy init dashscope."""
        if self.api_key and DASHSCOPE_AVAILABLE:
            import dashscope
            dashscope.api_key = self.api_key
    
    def get_available_voices(self) -> dict:
        """Get available system voices."""
        return self.VOICES
    
    async def synthesize(
        self,
        text: str,
        voice: str = "longanyang",
        speech_rate: float = 1.0,
        pitch_rate: float = 1.0,
    ) -> dict:
        """
        Synthesize speech with CosyVoice.
        
        Args:
            text: Text to speak
            voice: Voice name from available voices
            speech_rate: Speed (0.5-2.0)
            pitch_rate: Pitch (0.5-2.0)
            
        Returns:
            Dict with audio data and metadata
        """
        if not self.api_key:
            return {"error": "No API key configured", "audio_url": None}
        
        if not DASHSCOPE_AVAILABLE:
            return {"error": "dashscope not installed", "audio_url": None}
        
        try:
            self._init_dashscope()
            from dashscope.audio.tts_v2 import SpeechSynthesizer
            
            synth = SpeechSynthesizer(
                model='cosyvoice-v3-flash',
                voice=voice,
                speech_rate=speech_rate,
                pitch_rate=pitch_rate,
            )
            audio_bytes = synth.call(text)
            
            return {
                "audio": audio_bytes,
                "duration": len(text) * 0.3,  # estimate
                "voice": voice,
                "text": text,
            }
        except Exception as e:
            return {"error": str(e), "audio_url": None}
    
    async def synthesize_to_file(
        self,
        text: str,
        output_path: str,
        voice: str = "longanyang",
        speech_rate: float = 1.0,
        pitch_rate: float = 1.0,
    ) -> dict:
        """Synthesize speech and save to file."""
        result = await self.synthesize(text, voice, speech_rate, pitch_rate)
        
        if result.get("audio"):
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(result["audio"])
            return {
                "audio_url": output_path,
                "duration": result.get("duration"),
                "voice": voice,
            }
        return result


# Singleton instance
cosyvoice_service = CosyVoiceService()


def get_cosyvoice_service() -> CosyVoiceService:
    """Get initialized CosyVoice service."""
    from app.core.config import settings
    if settings.dashscope_api_key:
        cosyvoice_service.api_key = settings.dashscope_api_key
    return cosyvoice_service