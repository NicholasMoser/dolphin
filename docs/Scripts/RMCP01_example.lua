-- Example script for use with RMCP01 (Mario Kart Wii PAL)

-- General purpose registers
for i = 0, 31, 1 do
  print(string.format("gpr[%d] = %x", i, dolphin.ppc.gpr[i]))
end
print(string.format("pc = %x", dolphin.ppc.pc))

-- Paired single registers
for i = 0, 31, 1 do
  ps_reg = dolphin.ppc.ps_f64[i]
  print(string.format("ps[%d][0] = %f", i, ps_reg[0]))
  print(string.format("ps[%d][1] = %f", i, ps_reg[1]))
end

-- Basic memory access
print(dolphin.mem_read(0x80000000, 6))
if dolphin.mem_u32[0x80000000] ~= 0x524d4350 then
  error("Not running RMCP01")
end

-- Basic instruction hooks
main_hook = function ()
  print("main")
end
dolphin.hook_instruction(0x80008ef0, main_hook)
dolphin.hook_instruction(0x80008ef0, main_hook) -- should be no-op

-- Log something
layouts = {}
dolphin.hook_instruction(0x805e889c, function ()
  lyt_name_ptr = dolphin.ppc.gpr[4]
  lyt_name = dolphin.str_read(lyt_name_ptr, 100)
  if layouts[lyt_name] == nil then
    print(lyt_name)
    layouts[lyt_name] = true
  end
end)

-- Print frame count every now and then
frame_count = 0
dolphin.hook_frame(function ()
  frame_count = frame_count + 1
  if frame_count % 120 == 0 then
    print("frame " .. frame_count)
  end
end)

-- EFB frame dumping
x_steps = 0
dolphin.hook_instruction(0x8006910c, function ()
  x_steps = x_steps + 1
  print("Dumping EFB")
  x = dolphin.dump_efb()
  file = io.open(string.format("efbtest-%06d", x_steps), "w")
  file:write(x)
  io.close(file)
end)
