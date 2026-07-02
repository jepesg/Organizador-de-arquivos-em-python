from pathlib import Path
import shutil
from typing import Iterable

# função para criar a pasta com base na extensão
def get_folder_name(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")

    mapping = {
        "png": "Imagens",
        "jpg": "Imagens",
        "jpeg": "Imagens",
        "gif": "Imagens",
        "bmp": "Imagens",
        "svg": "Imagens",
        "webp": "Imagens",
        "pdf": "PDF",
        "doc": "Documentos",
        "docx": "Documentos",
        "txt": "Documentos",
        "rtf": "Documentos",
        "xlsx": "Documentos",
        "xls": "Documentos",
        "ppt": "Documentos",
        "pptx": "Documentos",
        "csv": "Documentos",
        "zip": "Comprimidos",
        "rar": "Comprimidos",
        "7z": "Comprimidos",
        "tar": "Comprimidos",
        "gz": "Comprimidos",
        "mp3": "Musica",
        "wav": "Musica",
        "flac": "Musica",
        "mp4": "Videos",
        "avi": "Videos",
        "mkv": "Videos",
        "mov": "Videos",
        "wmv": "Videos",
        "exe": "Programas",
        "msi": "Programas",
        "apk": "Programas",
        "iso": "Imagens",
    }
#   Return para criar a pasta com base na extensão
    return mapping.get(ext, "Outros")

# Função para ler todos os arquivos e organizar
def get_files_to_organize(directory: Path) -> list[Path]:
    return [path for path in directory.iterdir() if path.is_file()]

# Função para organizar os arquivos
def organize_files(
    directory: str | None = None,
    *,
    skip_files: Iterable[str] = (),
    return_details: bool = False,
) -> int | tuple[int, list[tuple[str, str]]]: # int| tuple para informar a quantidade de arquivos
    target_dir = Path(directory).resolve() if directory else Path.cwd().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    moved = 0
    skip_names = set(skip_files)
    organized_files: list[tuple[str, str]] = []
#   For para ler cada arquivo e reorganizar nas pastas
    for path in get_files_to_organize(target_dir):
        if path.name in skip_names:
            continue

        folder_name = get_folder_name(path)
        folder_path = target_dir / folder_name
        folder_path.mkdir(exist_ok=True)

        destination = folder_path / path.name
        if destination.exists():
            stem = path.stem
            suffix = path.suffix
            counter = 1
            while destination.exists():
                destination = folder_path / f"{stem}_{counter}{suffix}"
                counter += 1

        shutil.move(str(path), str(destination))
        organized_files.append((path.name, folder_name))
        moved += 1
#   Return para mostrar quantidade de arqiuvos
    if return_details:
        return moved, organized_files
    return moved

# Função para gerar um log com data de organização e quais arquivos foram organizadas
def generate_log(moved: int, organized_files: list[tuple[str, str]]) -> None:
    desktop_path = Path.home() / "Documentos"
    log_file = desktop_path / "organizador_log.txt"
#   With para criar o log na area de trabalho
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"Arquivos organizados: {moved}\n")
        for file_name, folder_name in organized_files:
            f.write(f"- {file_name} -> {folder_name}\n")
        f.write("\n")

#   If__name__ executa a função de organização dos arquivos
if __name__ == "__main__":
    moved, organized_files = organize_files(skip_files={Path(__file__).name}, return_details=True)
    print("Arquivos organizados:")
    for file_name, folder_name in organized_files:
        print(f"- {file_name} -> {folder_name}")
    print(f"Total: {moved}")
    generate_log(moved, organized_files)



