# data-structures-multi-compiler

Universal data structure compiler supporting 12 programming languages with ARM64 and x86_64 cross-compilation.

## Overview

This project provides a unified build system that can compile data structure implementations in all 12 supported languages:

- **Rust** - cargo, rustc
- **Go** - go build
- **C** - gcc (GNU), clang (LLVM)
- **C++** - g++ (GNU), clang++ (LLVM)
- **Perl** - perl
- **Ruby** - ruby, mruby
- **C#** - dotnet, mono
- **JavaScript** - node, deno
- **TypeScript** - tsc, ts-node
- **Python** - python, pypy, cython
- **Java** - javac, graalvm
- **Swift** - swiftc
- **Objective-C** - clang, gcc-objc

## Architecture Support

### ARM64 (Apple Silicon / AArch64)
- Native compilation on ARM64 hosts
- Cross-compilation from x86_64 to ARM64
- GNU toolchain: `aarch64-linux-gnu-gcc`
- LLVM toolchain: `clang --target=aarch64`

### x86_64 (AMD64)
- Native compilation on x86_64 hosts
- Cross-compilation from ARM64 to x86_64
- GNU toolchain: `gcc`, `g++`
- LLVM toolchain: `clang`, `clang++`

## Compiler Preferences

| Language | Primary (GNU) | Alternative (LLVM/musl) |
|----------|--------------|------------------------|
| C | gcc | clang |
| C++ | g++ | clang++ |
| Rust | rustc (LLVM) | rustc (musl) |
| Go | go (gc) | go (gccgo) |
| Objective-C | gcc-objc | clang |
| Swift | swiftc (LLVM) | - |
| Java | OpenJDK | GraalVM |
| C# | dotnet | mono |
| Python | CPython | PyPy, Cython |
| JavaScript | Node.js | Deno |
| TypeScript | tsc | - |
| Perl | perl | - |
| Ruby | ruby | mruby |

## Quick Start

### Build All Languages

```bash
# Build all data structures for all languages
./build.sh --all

# Build specific language
./build.sh --lang rust
./build.sh --lang cpp
./build.sh --lang go

# Build for specific architecture
./build.sh --arch arm64
./build.sh --arch x86_64

# Cross-compile
./build.sh --target arm64 --host x86_64
```

### Build Individual Projects

```bash
# C/C++ with GNU compilers
make CC=gcc CXX=g++ ARCH=arm64

# C/C++ with LLVM compilers
make CC=clang CXX=clang++ ARCH=x86_64

# Rust
cargo build --target aarch64-unknown-linux-gnu
cargo build --target x86_64-unknown-linux-gnu

# Go
GOARCH=arm64 go build ./...
GOARCH=amd64 go build ./...

# Java
mvn package
native-image --target=arm64 -jar target/*.jar

# Python
python -m build
cythonize -i src/*.pyx

# TypeScript
tsc --project tsconfig.json
```

## Project Structure

```
data-structures-multi-compiler/
├── src/
│   ├── compilers/       # Compiler wrapper implementations
│   ├── builders/        # Build system implementations
│   └── schemas/         # Data structure schemas
├── toolchains/
│   ├── arm64/           # ARM64 toolchain configs
│   └── x86_64/          # x86_64 toolchain configs
├── docs/                # Documentation
├── examples/            # Example implementations
└── tests/               # Test suite
```

## Toolchain Setup

### ARM64 Toolchain (on x86_64 host)

```bash
# GNU toolchain
sudo apt-get install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu

# LLVM toolchain
sudo apt-get install clang lld

# Rust target
rustup target add aarch64-unknown-linux-gnu

# Go cross-compile (built-in)
GOARCH=arm64 go build
```

### x86_64 Toolchain (on ARM64 host)

```bash
# GNU toolchain
sudo apt-get install gcc-x86-64-linux-gnu g++-x86-64-linux-gnu

# LLVM toolchain
sudo apt-get install clang lld

# Rust target
rustup target add x86_64-unknown-linux-gnu

# Go cross-compile (built-in)
GOARCH=amd64 go build
```

## Compiler Wrappers

The project provides unified compiler wrappers that handle:

1. **Language detection** - Automatic language detection from file extensions
2. **Architecture targeting** - ARM64/x86_64 cross-compilation
3. **Toolchain selection** - GNU vs LLVM selection
4. **Optimization levels** - Debug, Release, ReleaseWithDebInfo
5. **Linking** - Static vs dynamic linking

## License

MIT License
