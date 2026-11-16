# PDFium for Cromo

Read PDF documents from a [Cromo](https://cromolang.org) program, with [PDFium](https://pdfium.googlesource.com/pdfium/), the engine of Chrome: the pages, their text, and each page as a picture.

```sh
cromo get github.com/cromolang/pdfium
```

```cromo
import pdfium
import std.fs

i32 main() {
    pdfium.Document report = pdfium.load("report.pdf")
    println("{} pages; the first says: {}", report.pageCount(), report.text(0))
    pdfium.Picture page = report.render(0, 1200)   // 1200 pixels wide
    fs.writeBytes("page1.bmp", page.bmp())
    ret 0
}
```

There is nothing else to install. The library of PDFium is the one of the project [pdfium-binaries](https://github.com/bblanchon/pdfium-binaries), built from the sources of PDFium: `cromo` downloads it the first time the program is built, checks it by its hash, and puts it next to the executable, `pdfium.dll` on Windows and `libpdfium.so` on Linux. A program is given to others with that file next to it.

## What it has

- `pdfium.load(path)` opens a file, and `pdfium.Document(bytes)` its bytes, as those of `embed("manual.pdf")`.
- `document.pageCount()`, and `pageWidth(i)` and `pageHeight(i)` in points: 72 are an inch, and an A4 page is 595 by 842. The pages are from 0.
- `document.text(i)` is the text of a page; `""` for a page of images only, as a scan.
- `document.render(i, width)` draws a page `width` pixels wide, on white, and gives a `pdfium.Picture`: its `width`, its `height` and its `pixels`, four bytes each, red, green, blue and 255.
- `picture.bmp()` is the picture as a BMP file, which `gui.ImageBox.setBytes` shows in a window of `std.gui` and every program of images opens.
- `document.info("Title")` is what the document says of itself: `Title`, `Author`, `Subject`, `Keywords`, `Creator`, `Producer`.

A file that is not a PDF, or that asks for a password, is an `Error` that says which. A page that the document does not have is a panic.

## Limits of this version

- It reads: it does not write or change a PDF.
- Documents with a password are refused.
- PDFium works on one thread at a time: a program that reads documents from more threads takes turns.
- Windows and Linux on x86-64.

## The versions

| This package | PDFium | Cromo |
|---|---|---|
| v0.1.0 | 159.0.8152.0 (chromium/8152) | 0.90 or later |

## Developing it

```sh
cromo test pdfium.cro
python tools/sample.py testdata/sample.pdf   # writes the document of the tests again
```

## License

MIT: see `LICENSE`. PDFium is a work of Google and of the authors of PDFium and Foxit, under the Apache License 2.0 and BSD licenses, which are in the archives of pdfium-binaries.
