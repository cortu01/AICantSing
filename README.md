# AI Can't Sing 🎤🎨

## Summary & Concept

**AI Can't Sing** is an interactive AI-powered music visualization system that generates real-time artwork based on your voice input. The system listens to your speech through a microphone, transcribes it using OpenAI's Whisper API, and creates unique digital artwork using either OpenAI's DALL-E 3 or a local Stable Diffusion model.

Local models drawn from the AI & Storytelling course, which can be found here: [aist.cortu01.com](https://aist.cortu01.com).

### Key Features
- **Real-time voice transcription** using OpenAI Whisper
- **Dual image generation**: Choose between OpenAI DALL-E 3 or local Stable Diffusion
- **Live audio capture** with configurable recording duration
- **Automatic image display** in dedicated windows
- **Pause/resume functionality** with F8/F9 hotkeys
- **Artist/song context** for enhanced image generation
- **Starter image display** for immediate visual feedback

## Installation Instructions

### Prerequisites
- Python 3.9+
- macOS (tested on Apple Silicon Macs)
- Microphone access
- OpenAI API key (for DALL-E and Whisper)

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone <your-repo-url>
   cd AICantSing
   ```

2. **Install Python dependencies**
   - Open `AICantSing.ipynb` in Jupyter Notebook
   - Run **Cell 0** to install basic packages
   - Run **Cell 1** to install AI model dependencies

3. **Run promo cells first** (Cells 2 and 3)
   - This avoids crashes that can occur when running them later
   - Run these cells, then restart the kernel

4. **Configure cache location** (Cell 4)
   - This sets up Hugging Face cache to avoid permission issues
   - Creates cache in `~/Documents/huggingface_cache`

5. **Install AI storytelling models** (Cell 5)
   - Installs the local Stable Diffusion models
   - May take several minutes on first run

6. **Set up environment variables**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     MY_API_KEY=your_openai_api_key_here
     ```

7. **Configure microphone**
   - Run **Cell 10** to identify your microphone
   - Note the device index and update `DEVICE_INDEX` in the main loop

### Important Notes
- **First run**: Local models will download ~4GB of files (one-time)
- **GPU acceleration**: Configured for Apple Silicon (MPS) by default
- **Cache permissions**: May need to run `chmod -R 755 ~/.cache/huggingface/hub` if you encounter permission errors
- **Locale fix**: If you see encoding errors, update the locale line in Cell 5
- **Promo images**: Run Cells 2 and 3 first (chance of crash; will work on second try), then run further setup cells

## File Structure

### Core Files
- **`AICantSing.ipynb`**: Main Jupyter notebook with all functionality
- **`utils.py`**: Utility functions for image generation and display
- **`AICantSing.py`**: Standalone Python version (alternative to notebook)

### Configuration
- **`.env`**: Environment variables (API keys, paths)
- **`starter.png`**: Initial image displayed when system starts

### Generated Content
- **`generated_images/`**: Folder where all generated images are saved
- **`promo1.png` & `promo2.png`**: Promotional QR codes displayed during operation

### Dependencies
- **`requirements.txt`**: Python package dependencies (if using pip)
- **`.gitignore`**: Git ignore rules (excludes generated images, cache, etc.)

## Usage Guide

### Starting the System
1. **First run**: Execute promo cells (2 and 14) to avoid crashes, then restart kernel
2. Run all setup cells in order (0, 1, 4-10)
3. Load the starter image (Cell 3)
4. Test API key (Cells 11-12)
5. Run the main loop (Cell 15)

### Controls
- **F8**: Pause the system
- **F9**: Resume the system
- **Ctrl+C**: Stop the main loop

### Model Selection
In the main loop, you can choose between:
- **Local model**: `USE_LOCAL_MODEL = True` (free, ~25 seconds)
- **OpenAI DALL-E**: `USE_LOCAL_MODEL = False` (paid, ~15 seconds)

### Customization
- **Recording duration**: Modify `duration=3` in `record_audio()` call
- **Sleep time**: Adjust `time.sleep(0.3)` between cycles
- **Image quality**: Change `rounds=3` for local model speed/quality trade-off
- **Window position**: Modify `IMAGE_WINDOW_X` and `IMAGE_WINDOW_Y` in `utils.py`

## Performance Tips

### Speed Optimization
- **Local model**: Reduce `rounds` parameter (3-5 for speed, 20+ for quality)
- **Recording**: Reduce `duration` from 3 to 2 seconds
- **Sleep time**: Reduce from 0.3 to 0.1 seconds between cycles

### Quality vs Speed
- **DALL-E 3**: Best quality, fastest generation, costs money
- **Local Stable Diffusion**: Good quality, slower, completely free
- **Rounds parameter**: Lower = faster but less detailed

## Troubleshooting

### Common Issues
1. **Permission errors**: Run `chmod -R 755 ~/.cache/huggingface/hub`
2. **Microphone not found**: Check `DEVICE_INDEX` in main loop
3. **API key errors**: Verify `.env` file and API key validity
4. **Model loading errors**: Restart kernel and run setup cells in order
5. **MPS/GPU errors**: Set `accelerate=False` in local model calls
6. **Promo image crashes**: Run promo cells (2 and 14) first, then restart kernel

### Performance Issues
- **Slow local generation**: Reduce `rounds` parameter
- **High memory usage**: Close other applications
- **Network timeouts**: Check internet connection for DALL-E

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Test changes thoroughly
4. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add comments for complex logic
- Update documentation for new features

## Acknowledgments

- OpenAI for DALL-E 3 and Whisper APIs
- Hugging Face for Stable Diffusion models
- AI & Storytelling course for local model integration
- PyAudio for audio capture functionality

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the error messages in the notebook output
- Ensure all dependencies are properly installed
- Verify your OpenAI API key is valid and has sufficient credits

---

**Note**: This system requires an active internet connection for OpenAI API calls and may incur costs depending on your usage of DALL-E 3 and Whisper services. (Local transcription model option to follow in future update).
