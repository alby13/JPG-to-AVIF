# JPG to AVIF Converter

A powerful, user-friendly desktop application for converting JPEG, PNG, and other images to the modern AVIF format with real-time preview and quality adjustment.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- **Real-time Preview**: See exactly how your AVIF conversion will look before saving
- **Live Quality Adjustment**: Interactive slider to adjust compression quality (0-100)
- **Multiple Input Methods**: 
  - Drag & drop files directly into the application
  - Traditional file browser selection
  - Paste images directly from clipboard (Ctrl+V)
- **Format Support**: Convert from PNG, JPEG, BMP, and WebP formats
- **Responsive UI**: Automatically scales preview to fit window size
- **File Size Preview**: Shows compressed file size in real-time
- **High-Quality Output**: Uses optimized AVIF encoding for final saves

## 🚀 Why AVIF?

AVIF (AV1 Image File Format) is a modern image format that offers:
- **Superior compression**: Up to 80% smaller files than JPEG
- **Better quality**: Maintains visual fidelity at lower file sizes
- **Modern features**: Supports HDR, wide color gamut, and transparency
- **Future-proof**: Growing browser and application support

## 📋 Requirements

- Python 3.7+
- Required packages (install via pip):
  ```bash
  pip install pillow pillow-avif tkinterdnd2
  ```

## 🛠️ Installation

#### You can download the Windows Executable in the releases section.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alby13/JPG-to-AVIF
   cd JPG-to-AVIF
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python avif_converter.py
   ```

## 💡 Usage

### Getting Started
1. Launch the application
2. Load an image using one of these methods:
   - **Drag & Drop**: Drag an image file into the preview area
   - **File Browser**: Click "Select Image" to browse for files
   - **Clipboard**: Press `Ctrl+V` to paste an image from clipboard

### Adjusting Quality
- Use the quality slider to see real-time changes
- **0-30**: Very high compression, smaller files, lower quality
- **50-70**: Balanced compression and quality (recommended)
- **80-100**: Minimal compression, larger files, highest quality

### Saving Your Image
- Click "Save AVIF File" when satisfied with the preview
- Choose your save location and filename
- The final save uses optimized compression settings for best results

## 🖥️ Interface Overview

```
┌─────────────────────────────────────────┐
│                                         │
│           Image Preview Area            │
│        (Drag & Drop Supported)          │
│                                         │
├─────────────────────────────────────────┤
│ AVIF Quality: ████████░░ 75             │
├─────────────────────────────────────────┤
│ [Select Image] [Save AVIF File]         │
├─────────────────────────────────────────┤
│ Status: Previewing at 85% (245.3 KB)    │
└─────────────────────────────────────────┘
```

## 📁 Project Structure

```
live-avif-converter/
├── jpgtoavif.py      # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── LICENSE               # License
```

## 🔧 Dependencies

- **Pillow**: Image processing library
- **pillow-avif**: AVIF format support for Pillow  
- **tkinterdnd2**: Drag and drop functionality for Tkinter

## 🐛 Known Issues & Limitations

- **Transparency**: Currently converts images to RGB (transparency support can be added)
- **Very Large Images**: May require significant RAM for processing
- **AVIF Support**: Requires system-level AVIF codec support

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

1. **Report bugs** by opening an issue
2. **Suggest features** or improvements  
3. **Submit pull requests** with bug fixes or new features
4. **Improve documentation** or add examples

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📝 Changelog

### v1.0.0 (Current)
- Initial release
- Real-time AVIF preview
- Quality adjustment slider
- Drag & drop support
- Clipboard paste functionality
- Multi-format input support

## 🔮 Roadmap

- [ ] Batch conversion support
- [ ] Transparency/alpha channel preservation  
- [ ] Additional output formats (WebP, JPEG XL)
- [ ] Command-line interface
- [ ] Progress bars for large files
- [ ] Preset quality configurations
- [ ] Image metadata preservation

## 📄 License

Details of license to follow.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- AVIF support provided by [pillow-avif](https://github.com/fdintino/pillow-avif)
- Drag & drop functionality via [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)

---

⭐ **Star this repository** if you find it helpful!
