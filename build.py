#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Optional

ALL_LANGUAGES = [
    "rust",
    "go",
    "c",
    "cpp",
    "perl",
    "ruby",
    "csharp",
    "javascript",
    "typescript",
    "python",
    "java",
    "swift",
    "objective-c",
]

ARCHITECTURES = ["arm64", "x86_64"]


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> int:
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode


def build_rust(arch: str, build_type: str) -> int:
    target_map = {
        "arm64": "aarch64-unknown-linux-gnu",
        "x86_64": "x86_64-unknown-linux-gnu",
    }
    target = target_map[arch]
    profile = "release" if build_type == "release" else "dev"
    return run_command(["cargo", "build", f"--profile={profile}", f"--target={target}"])


def build_go(arch: str, build_type: str) -> int:
    go_arch = "arm64" if arch == "arm64" else "amd64"
    env = os.environ.copy()
    env["GOARCH"] = go_arch
    cmd = ["go", "build"]
    if build_type == "release":
        cmd.extend(["-ldflags", "-s -w"])
    cmd.append("./...")
    return run_command(cmd)


def build_c(arch: str, build_type: str) -> int:
    cflags = "-Wall -Wextra"
    if arch == "arm64":
        cflags += " -target aarch64-linux-gnu"
    else:
        cflags += " -target x86_64-linux-gnu"
    if build_type == "release":
        cflags += " -O3"
    else:
        cflags += " -g -O0"
    return run_command(["make", f"CFLAGS={cflags}", f"ARCH={arch}"])


def build_cpp(arch: str, build_type: str) -> int:
    cxxflags = "-Wall -Wextra -std=c++17"
    if arch == "arm64":
        cxxflags += " -target aarch64-linux-gnu"
    else:
        cxxflags += " -target x86_64-linux-gnu"
    if build_type == "release":
        cxxflags += " -O3"
    else:
        cxxflags += " -g -O0"
    return run_command(["make", f"CXXFLAGS={cxxflags}", f"ARCH={arch}"])


def build_python(arch: str, build_type: str) -> int:
    result = run_command(["python", "-m", "build"])
    if result == 0 and Path("src").exists():
        for pyx in Path("src").rglob("*.pyx"):
            run_command(["cythonize", "-i", str(pyx)])
    return result


def build_java(arch: str, build_type: str) -> int:
    result = run_command(["mvn", "clean", "package", "-DskipTests"])
    if result == 0:
        jars = list(Path("target").glob("*.jar"))
        if jars and shutil.which("native-image"):
            runtime = "arm64" if arch == "arm64" else "amd64"
            run_command(["native-image", f"--target={runtime}", "-jar", str(jars[0])])
    return result


def build_javascript(arch: str, build_type: str) -> int:
    if Path("package.json").exists():
        run_command(["npm", "install"])
        return run_command(["npm", "run", "build"])
    return 0


def build_typescript(arch: str, build_type: str) -> int:
    if Path("tsconfig.json").exists():
        return run_command(["tsc", "--project", "tsconfig.json"])
    return 0


def build_csharp(arch: str, build_type: str) -> int:
    config = "Release" if build_type == "release" else "Debug"
    runtime = "linux-arm64" if arch == "arm64" else "linux-x64"
    return run_command(["dotnet", "build", "-c", config, "-r", runtime])


def build_ruby(arch: str, build_type: str) -> int:
    if Path("Gemfile").exists():
        run_command(["bundle", "install"])
    if Path("Rakefile").exists():
        return run_command(["rake"])
    return 0


def build_perl(arch: str, build_type: str) -> int:
    if Path("Makefile.PL").exists():
        run_command(["perl", "Makefile.PL"])
        return run_command(["make"])
    elif Path("Build.PL").exists():
        run_command(["perl", "Build.PL"])
        return run_command(["./Build"])
    return 0


def build_swift(arch: str, build_type: str) -> int:
    config = "release" if build_type == "release" else "debug"
    return run_command(["swift", "build", "-c", config])


def build_objective_c(arch: str, build_type: str) -> int:
    cflags = "-Wall -Wextra -fobjc-arc"
    if arch == "arm64":
        cflags += " -target aarch64-linux-gnu"
    else:
        cflags += " -target x86_64-linux-gnu"
    if build_type == "release":
        cflags += " -O3"
    else:
        cflags += " -g -O0"
    return run_command(["make", f"CFLAGS={cflags}", f"ARCH={arch}", "OBJC=1"])


BUILDERS = {
    "rust": build_rust,
    "go": build_go,
    "c": build_c,
    "cpp": build_cpp,
    "python": build_python,
    "java": build_java,
    "javascript": build_javascript,
    "typescript": build_typescript,
    "csharp": build_csharp,
    "ruby": build_ruby,
    "perl": build_perl,
    "swift": build_swift,
    "objective-c": build_objective_c,
}


def main():
    parser = argparse.ArgumentParser(
        description="Multi-language data structures compiler"
    )
    parser.add_argument("--all", action="store_true", help="Build all languages")
    parser.add_argument(
        "--lang",
        action="append",
        dest="languages",
        choices=ALL_LANGUAGES,
        help="Build specific language (can be used multiple times)",
    )
    parser.add_argument(
        "--arch", choices=ARCHITECTURES, default=None, help="Target architecture"
    )
    parser.add_argument(
        "--target",
        choices=ARCHITECTURES,
        default=None,
        help="Cross-compile target architecture",
    )
    parser.add_argument("--debug", action="store_true", help="Build in debug mode")
    parser.add_argument(
        "--release",
        action="store_true",
        default=True,
        help="Build in release mode (default)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    languages = args.languages or []
    if args.all:
        languages = ALL_LANGUAGES

    if not languages:
        parser.error("No languages specified. Use --all or --lang <language>")

    import platform

    arch = (
        args.arch
        or args.target
        or ("arm64" if platform.machine() in ("aarch64", "arm64") else "x86_64")
    )
    build_type = "debug" if args.debug else "release"

    print(f"Building: {', '.join(languages)}")
    print(f"Architecture: {arch}")
    print(f"Build type: {build_type}")

    for lang in languages:
        print(f"\n{'=' * 50}")
        print(f"Building {lang}...")
        print("=" * 50)
        result = BUILDERS[lang](arch, build_type)
        if result == 0:
            print(f"✓ Successfully built {lang}")
        else:
            print(f"✗ Failed to build {lang}")

    print("\nBuild complete!")


if __name__ == "__main__":
    main()
