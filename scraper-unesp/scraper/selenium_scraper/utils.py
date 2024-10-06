"""
File and Document Conversion Utilities Module

This module provides utility functions for file operations and document conversions.
It includes functions for saving files, converting documents between different formats,
and handling PDF files.

Functions:
- save_file: Save content to a file in a specified directory.
- convert_doc_to_pdf: Convert a .doc file to PDF format using LibreOffice.
- convert_pdf_to_markdown: Convert a PDF file to Markdown format.
- convert_pdf_to_png: Convert a PDF file to a series of PNG images, one per page.

These utilities are designed to work with pathlib.Path objects for consistent
and Pythonic file path handling.

Dependencies:
- subprocess: For running external commands (LibreOffice).
- pathlib: For file and directory path operations.
- pymupdf: For PDF file operations.
- pymupdf4llm: For PDF to Markdown conversion.

Note: Ensure that LibreOffice is installed and accessible via the 'soffice' command
for the convert_doc_to_pdf function to work properly.
"""

import subprocess
from pathlib import Path
import pymupdf
import pymupdf4llm

def save_file(
        file_name: str,
        output_directory: str | Path,
        content: str
        ) -> Path:
    """
    Save content to a file in the specified directory.

    Args:
        file_name (str): Name of the file to create.
        output_directory (Path): Directory to save the file in.
        content (str): Content to write to the file.

    Returns:
        Path: Path to the saved file.

    Raises:
        FileNotFoundError: If the output directory doesn't exist.
        FileExistsError: If the file already exists.
    """
    if not isinstance(output_directory, Path):
        output_directory = Path(output_directory)

    file_path = output_directory.joinpath(file_name)

    if not output_directory.exists():
        raise FileNotFoundError(f"Path {output_directory.resolve()} does not exists")

    if file_path.exists():
        raise FileExistsError(f"File {file_path} already exists")

    file_path.write_text(content, encoding="utf-8")

    return file_path


def convert_doc_to_pdf(
        doc_file_path: str | Path,
        output_directory: str | Path
) -> Path | None:
    """
    Convert a .doc file to PDF using LibreOffice.

    Args:
        doc_path (Path): Path to the .doc file.
        output_dir (Path): Directory to save the PDF file.

    Returns:
        Path: Path to the created PDF file.

    Raises:
        FileNotFoundError: If the PDF file was not created.
        subprocess.CalledProcessError: If the conversion process fails.
    """

    if not isinstance(doc_file_path, Path):
        doc_file_path = Path(doc_file_path)

    if not isinstance(output_directory, Path):
        output_directory = Path(output_directory)

    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_directory.resolve()),
        str(doc_file_path.resolve()),
    ], check=True)

    pdf_file_path = output_directory.joinpath(f"{doc_file_path.stem}.pdf")

    if not pdf_file_path.is_file():
        raise FileNotFoundError(f"PDF file {pdf_file_path} was not created")

    return pdf_file_path

def convert_pdf_to_markdown(
        pdf_file_path: str | Path,
        output_directory: str | Path
        ) -> Path:
    """
    Convert a PDF file to Markdown format.

    Args:
        pdf_path (Path): Path to the PDF file.
        output_dir (Path): Directory to save the Markdown file.

    Returns:
        Path: Path to the created Markdown file.
    """

    if not isinstance(pdf_file_path, Path):
        pdf_file_path = Path(pdf_file_path)

    if not isinstance(output_directory, Path):
        output_directory = Path(output_directory)

    md_content = pymupdf4llm.to_markdown(pdf_file_path)

    md_file_name = f"{pdf_file_path.stem}.md"

    md_file_path = save_file(
        file_name=md_file_name,
        output_directory=output_directory,
        content=md_content
    )

    return md_file_path

def convert_pdf_to_png(
        pdf_file_path: str | Path,
        output_directory: str | Path
        ) -> list[str]:
    """
    Convert a PDF file to PNG images, one per page.

    Args:
        pdf_path (Path): Path to the PDF file.
        output_dir (Path): Directory to save the PNG files.

    Returns:
        list[Path]: List of paths to the created PNG files.
    """
    image_paths = []
    if not isinstance(pdf_file_path, Path):
        pdf_file_path = Path(pdf_file_path)

    if not isinstance(output_directory, Path):
        output_directory = Path(output_directory)

    pdf_file = pymupdf.open(pdf_file_path)
    for page in pdf_file:
        pix = page.get_pixmap()
        img_file_path = output_directory.joinpath(
            pdf_file_path.stem + f"_page-{page.number}.png"
        )
        pix.save(f"{img_file_path}")
        image_paths.append(str(img_file_path.resolve()))
    return image_paths
