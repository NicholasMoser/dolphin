# Lua Scripts

Dolphin ships support for Lua 5.3 scripts that run embedded with the emulator.

*Caution:* Never run untrusted scripts or scripts you do not understand yourself!
Scripts will have access to your system like any other program, including the ability to do nasty things.

## Requirements

### Linux/OSX

Script support is disabled by default, and has to be enabled via CMake flag `-DLUA_SCRIPTS=true`.

It also requires Lua sources while compiling and the Lua 5.3 dynamic library at runtime.
Debian provides both with the `liblua5.3-dev` and `lua5.3` packages.

### Windows

Script support is disabled by default, and has to be enabled through a few different steps.

First, script support requires the Windows library for Lua 5.3. Go to the [Lua Binaries page](http://luabinaries.sourceforge.net/)
and select the latest release of 5.3. Select **Windows Libraries**, then select **Static**, and download the latest Win64 release
(e.g. `lua-5.3.5_Win64_vc16_lib`).

Unzip the Lua zip file to the `Externals` directory and rename it `lua`. Then create a new directory in the `lua` directory
named `lib`. Move `lua53.lib` into the `lib` directory. Your `lua` folder should now have the following two files in the
following directory structure:

- Externals/lua/include/lua.hpp
- Externals/lua/lib/lua53.lib

Last, open `Source/VSProps/Base.props` and change the XML element `UseLuaScripts` to `true`.

## Usage

Scripts are defined in game properties and are run just before emulation starts.
Any Lua code blocks emulator progression.

## `dolphin` API reference

**In development:** There are no stability guarantees. The scripting API will change very likely in future versions of Dolphin.

Lua scripts use the `dolphin` module for interacting with the emulator.

### PowerPC state (`ppc.*`)

Inspect and manipulate PowerPC register state.

#### Registers

| identifier              | type             | description                        |
| ----------------------- | ---------------- | ---------------------------------- |
| `dolphin.ppc.gpr[x]`    | `u32[32]`        | GPRs (general purpose registers)   |
| `dolphin.ppc.pc`        | `u32`            | PC (program counter)               |
| `dolphin.ppc.npc`       | `u32`            | NPC (next program counter)         |
| `dolphin.ppc.sr[x]`     | `u32[16]`        | SRs (segment registers)            |
| `dolphin.ppc.spr[x]`    | `u32[1024]`      | SPRs (special purpose registers)   |
| `dolphin.ppc.ps_u32[x]` | `(u32, u32)[32]` | paired single registers (u32 mode) |
| `dolphin.ppc.ps_u64[x]` | `(u64, u64)[32]` | paired single registers (u64 mode) |
| `dolphin.ppc.ps_f64[x]` | `(f64, f64)[32]` | paired single registers (f64 mode) |

### Memory access

Access Wii memory from the main processor's view.

#### Memory arrays

Lua tables taking an address as index. Supports unaligned access.

| identifier            | type     | description               |
| --------------------- | -------- | ------------------------- |
| `dolphin.ppc.mem_u8`  | `u8[*]`  | Read/write u8             |
| `dolphin.ppc.mem_u16` | `u16[*]` | Read/write big-endian u16 |
| `dolphin.ppc.mem_u32` | `u32[*]` | Read/write big-endian u32 |
| `dolphin.ppc.mem_u64` | `u32[*]` | Read/write big-endian u64 |
| `dolphin.ppc.mem_f32` | `f32[*]` | Read/write big-endian f32 |
| `dolphin.ppc.mem_f64` | `f64[*]` | Read/write big-endian f64 |

#### Memory utility functions

##### `mem_read`

Reads bytes from memory.
* Argument 1: `number address`
* Argument 2: `number len`
* Returns `string`

##### `mem_write`

Writes bytes to memory.
* Argument 1: `number address`
* Argument 2: `string data`

##### `str_read`

Reads null-terminated string from memory, removing the null-terminator.
* Argument 1: `number address`
* Argument 2: `number max_len` (max length including null-terminator)
* Returns `string`

##### `str_write`

Writes string to memory with null-terminator.
* Argument 1 `number address`
* Argument 2 `string data`
* Argument 3 `number max_len` (max length including null-terminator)

### Script hooks

Script hooks attach Lua functions to run on emulator events.

#### Instruction hooks

Instruction hooks execute Lua functions just before an instruction at a specific address is executed.

Only works when Dolphin is in debug mode.

##### `hook_instruction`

Installs a Lua function to an instruction (breakpoint).
* Argument 1: `number address`
* Argument 2: Lua function (zero arguments, zero return values)

##### `unhook_instruction`

Uninstalls a previously installed Lua instruction hook.
Takes the same arguments as `hook_instruction`.

#### Frame hooks

Frame hooks execute Lua functions every time a video frame is rendered.

##### `hook_frame`

Installs a Lua function to run on every frame.
* Argument 1: Lua function (zero arguments, zero return values)

##### `unhook_frame`

Uninstalls a previously installed Lua frame hook.
Takes the same arguments as `hook_frame`.
