--[[
This script expects to receive JSON and will send JSON back. A message should
be a list of 1 or more requests which will be executed in order. Each request
will have a corresponding response in the same order.

Every individual request and response is a JSON object with at minimum one
field `type`. The value of `type` determines what other fields may exist.

To get the script version, instead of JSON, send "VERSION" to get the script
version directly (e.g. "1.2.0").

#### Ex. 1

Request: `[{"type": "PING"}]`

Response: `[{"type": "PONG"}]`

---

#### Ex. 2

Request: `[{"type": "LOCK"}, {"type": "HASH"}]`

Response: `[{"type": "LOCKED"}, {"type": "HASH_RESPONSE", "value": "F7D18982"}]`

---

#### Ex. 3

Request:

```json
[
    {"type": "GUARD", "address": 100, "expected_data": "aGVsbG8=", "domain": "System Bus"},
    {"type": "READ", "address": 500, "size": 4, "domain": "ROM"}
]
```

Response:

```json
[
    {"type": "GUARD_RESPONSE", "address": 100, "value": true},
    {"type": "READ_RESPONSE", "value": "dGVzdA=="}
]
```

---

#### Ex. 4

Request:

```json
[
    {"type": "GUARD", "address": 100, "expected_data": "aGVsbG8=", "domain": "System Bus"},
    {"type": "READ", "address": 500, "size": 4, "domain": "ROM"}
]
```

Response:

```json
[
    {"type": "GUARD_RESPONSE", "address": 100, "value": false},
    {"type": "GUARD_RESPONSE", "address": 100, "value": false}
]
```

---

### Supported Request Types

- `PING`  
    Does nothing; resets timeout.

    Expected Response Type: `PONG`

- `SYSTEM`  
    Returns the system of the currently loaded ROM (N64, GBA, etc...).

    Expected Response Type: `SYSTEM_RESPONSE`

- `PREFERRED_CORES`  
    Returns the user's default cores for systems with multiple cores. If the
    current ROM's system has multiple cores, the one that is currently
    running is very probably the preferred core.

    Expected Response Type: `PREFERRED_CORES_RESPONSE`

- `HASH`  
    Returns the hash of the currently loaded ROM calculated by BizHawk.

    Expected Response Type: `HASH_RESPONSE`

- `GUARD`  
    Checks a section of memory against `expected_data`. If the bytes starting
    at `address` do not match `expected_data`, the response will have `value`
    set to `false`, and all subsequent requests will not be executed and
    receive the same `GUARD_RESPONSE`.

    Expected Response Type: `GUARD_RESPONSE`

    Additional Fields:
    - `address`: The address of the memory to check
    - `expected_data`: A base64 string of contiguous data
    - `domain`: The name of the memory domain the address corresponds to

- `LOCK`  
    Halts emulation and blocks on incoming requests until an `UNLOCK` request
    is received or the client times out. All requests processed while locked
    will happen on the same frame.

    Expected Response Type: `LOCKED`

- `UNLOCK`  
    Resumes emulation after the current list of requests is done being
    executed.

    Expected Response Type: `UNLOCKED`

- `READ`  
    Reads an array of bytes at the provided address.

    Expected Response Type: `READ_RESPONSE`

    Additional Fields:
    - `address`: The address of the memory to read
    - `size`: The number of bytes to read
    - `domain`: The name of the memory domain the address corresponds to

- `WRITE`  
    Writes an array of bytes to the provided address.

    Expected Response Type: `WRITE_RESPONSE`

    Additional Fields:
    - `address`: The address of the memory to write to
    - `value`: A base64 string representing the data to write
    - `domain`: The name of the memory domain the address corresponds to

- `DISPLAY_MESSAGE`  
    Adds a message to the message queue which will be displayed using
    `gui.addmessage` according to the message interval.

    Expected Response Type: `DISPLAY_MESSAGE_RESPONSE`

    Additional Fields:
    - `message`: The string to display

- `SET_MESSAGE_INTERVAL`  
    Sets the minimum amount of time to wait between displaying messages.
    Potentially useful if you add many messages quickly but want players
    to be able to read each of them.

    Expected Response Type: `SET_MESSAGE_INTERVAL_RESPONSE`

    Additional Fields:
    - `value`: The number of seconds to set the interval to


### Response Types

- `PONG`  
    Acknowledges `PING`.

- `SYSTEM_RESPONSE`  
    Contains the name of the system for currently running ROM.

    Additional Fields:
    - `value`: The returned system name

- `PREFERRED_CORES_RESPONSE`  
    Contains the user's preferred cores for systems with multiple supported
    cores. Currently includes NES, SNES, GB, GBC, DGB, SGB, PCE, PCECD, and
    SGX.

    Additional Fields:
    - `value`: A dictionary map from system name to core name

- `HASH_RESPONSE`  
    Contains the hash of the currently loaded ROM calculated by BizHawk.

    Additional Fields:
    - `value`: The returned hash

- `GUARD_RESPONSE`  
    The result of an attempted `GUARD` request.

    Additional Fields:
    - `value`: true if the memory was validated, false if not
    - `address`: The address of the memory that was invalid (the same address
    provided by the `GUARD`, not the address of the individual invalid byte)

- `LOCKED`  
    Acknowledges `LOCK`.

- `UNLOCKED`  
    Acknowledges `UNLOCK`.

- `READ_RESPONSE`  
    Contains the result of a `READ` request.

    Additional Fields:
    - `value`: A base64 string representing the read data

- `WRITE_RESPONSE`  
    Acknowledges `WRITE`.

- `DISPLAY_MESSAGE_RESPONSE`  
    Acknowledges `DISPLAY_MESSAGE`.

- `SET_MESSAGE_INTERVAL_RESPONSE`  
    Acknowledges `SET_MESSAGE_INTERVAL`.

- `ERROR`  
    Signifies that something has gone wrong while processing a request.

    Additional Fields:
    - `err`: A description of the problem
]]

local base64 = require("base64")
local socket = require("socket")
local json = require("json")

-- Set to log incoming requests
-- Will cause lag due to large console output
local DEBUG = false

local SCRIPT_VERSION = 1

local SOCKET_PORT = 43055

local STATE_NOT_CONNECTED = 0
local STATE_CONNECTED = 1

local server = nil
local client_socket = nil

local current_state = STATE_NOT_CONNECTED

local timeout_timer = 0
local message_timer = 0
local message_interval = 0
local prev_time = 0
local current_time = 0

local locked = false

local rom_hash = nil

local lua_major, lua_minor = _VERSION:match("Lua (%d+)%.(%d+)")
lua_major = tonumber(lua_major)
lua_minor = tonumber(lua_minor)

if lua_major > 5 or (lua_major == 5 and lua_minor >= 3) then
    require("lua_5_3_compat")
end

local bizhawk_version = client.getversion()
local bizhawk_major, bizhawk_minor, bizhawk_patch = bizhawk_version:match("(%d+)%.(%d+)%.?(%d*)")
bizhawk_major = tonumber(bizhawk_major)
bizhawk_minor = tonumber(bizhawk_minor)
if bizhawk_patch == "" then
    bizhawk_patch = 0
else
    bizhawk_patch = tonumber(bizhawk_patch)
end

function queue_push (self, value)
    self[self.right] = value
    self.right = self.right + 1
end

function queue_is_empty (self)
    return self.right == self.left
end

function queue_shift (self)
    value = self[self.left]
    self[self.left] = nil
    self.left = self.left + 1
    return value
end

function new_queue ()
    local queue = {left = 1, right = 1}
    return setmetatable(queue, {__index = {is_empty = queue_is_empty, push = queue_push, shift = queue_shift}})
end

local message_queue = new_queue()

function lock ()
    locked = true
    client_socket:settimeout(2)
end

function unlock ()
    locked = false
    client_socket:settimeout(0)
end

function process_request (req)
    local res = {}

    if req["type"] == "PING" then
        res["type"] = "PONG"

    elseif req["type"] == "SYSTEM" then
        res["type"] = "SYSTEM_RESPONSE"
        res["value"] = emu.getsystemid()

    elseif req["type"] == "PREFERRED_CORES" then
        local preferred_cores = client.getconfig().PreferredCores
        res["type"] = "PREFERRED_CORES_RESPONSE"
        res["value"] = {}
        res["value"]["NES"] = preferred_cores.NES
        res["value"]["SNES"] = preferred_cores.SNES
        res["value"]["GB"] = preferred_cores.GB
        res["value"]["GBC"] = preferred_cores.GBC
        res["value"]["DGB"] = preferred_cores.DGB
        res["value"]["SGB"] = preferred_cores.SGB
        res["value"]["PCE"] = preferred_cores.PCE
        res["value"]["PCECD"] = preferred_cores.PCECD
        res["value"]["SGX"] = preferred_cores.SGX

    elseif req["type"] == "HASH" then
        res["type"] = "HASH_RESPONSE"
        res["value"] = rom_hash

    elseif req["type"] == "GUARD" then
        res["type"] = "GUARD_RESPONSE"
        local expected_data = base64.decode(req["expected_data"])

        local actual_data = memory.read_bytes_as_array(req["address"], #expected_data, req["domain"])

        local data_is_validated = true
        for i, byte in ipairs(actual_data) do
            if (byte ~= expected_data[i]) then
                data_is_validated = false
                break
            end
        end

        res["value"] = data_is_validated
        res["address"] = req["address"]

    elseif req["type"] == "LOCK" then
        res["type"] = "LOCKED"
        lock()

    elseif req["type"] == "UNLOCK" then
        res["type"] = "UNLOCKED"
        unlock()

    elseif req["type"] == "READ" then
        res["type"] = "READ_RESPONSE"
        res["value"] = base64.encode(memory.read_bytes_as_array(req["address"], req["size"], req["domain"]))

    elseif req["type"] == "WRITE" then
        res["type"] = "WRITE_RESPONSE"
        memory.write_bytes_as_array(req["address"], base64.decode(req["value"]), req["domain"])

    elseif req["type"] == "DISPLAY_MESSAGE" then
        res["type"] = "DISPLAY_MESSAGE_RESPONSE"
        message_queue:push(req["message"])

    elseif req["type"] == "SET_MESSAGE_INTERVAL" then
        res["type"] = "SET_MESSAGE_INTERVAL_RESPONSE"
        message_interval = req["value"]

    else
        res["type"] = "ERROR"
        res["err"] = "Unknown command: "..req["type"]
    end

    return res
end

-- Receive data from AP client and send message back
function send_receive ()
    local message, err = client_socket:receive()

    -- Handle errors
    if err == "closed" then
        if (current_state == STATE_CONNECTED) then
            print("Connection to client closed")
        end
        current_state = STATE_NOT_CONNECTED
        return
    elseif err == "timeout" then
        unlock()
        return
    elseif err ~= nil then
        print(err)
        current_state = STATE_NOT_CONNECTED
        unlock()
        return
    end

    -- Reset timeout timer
    timeout_timer = 5

    -- Process received data
    if DEBUG then
        print("Received Message ["..emu.framecount().."]: "..'"'..message..'"')
    end

    if message == "VERSION" then
        local result, err client_socket:send(tostring(SCRIPT_VERSION).."\n")
    else
        local res = {}
        local data = json.decode(message)
        local failed_guard_response = nil
        for i, req in ipairs(data) do
            if failed_guard_response ~= nil then
                res[i] = failed_guard_response
            else
                -- An error is more likely to cause an NLua exception than to return an error here
                local status, response = pcall(process_request, req)
                if status then
                    res[i] = response

                    -- If the GUARD validation failed, skip the remaining commands
                    if response["type"] == "GUARD_RESPONSE" and not response["value"] then
                        failed_guard_response = response
                    end
                else
                    res[i] = {type = "ERROR", err = response}
                end
            end
        end

        client_socket:send(json.encode(res).."\n")
    end
end

function main ()
    server, err = socket.bind("localhost", SOCKET_PORT)
    if (err ~= nil) then
        print(err)
        return
    end

    while true do
        current_time = socket.socket.gettime()
        timeout_timer = timeout_timer - (current_time - prev_time)
        message_timer = message_timer - (current_time - prev_time)
        prev_time = current_time

        if (message_timer <= 0 and not message_queue:is_empty()) then
            gui.addmessage(message_queue:shift())
            message_timer = message_interval
        end

        if (current_state == STATE_NOT_CONNECTED) then
            if (emu.framecount() % 60 == 0) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if (timeout == nil) then
                    print("Client connected")
                    current_state = STATE_CONNECTED
                    client_socket = client
                    client_socket:settimeout(0)
                else
                    print("No client found. Trying again...")
                end
            end
        else
            repeat
                send_receive()
            until not locked

            if (timeout_timer <= 0) then
                print("Client timed out")
                current_state = STATE_NOT_CONNECTED
            end
        end

        coroutine.yield()
    end
end

event.onexit(function ()
    print("\n-- Restarting Script --\n")
    if server ~= nil then
        server:close()
    end
end)

if bizhawk_major < 2 or (bizhawk_major == 2 and bizhawk_minor < 7) then
    print("Must use BizHawk 2.7.0 or newer")
elseif bizhawk_major > 2 or (bizhawk_major == 2 and bizhawk_minor > 9) then
    print("Warning: This version of BizHawk is newer than this script. If it doesn't work, consider downgrading to 2.9.")
else
    if emu.getsystemid() == "NULL" then
        print("No ROM is loaded. Please load a ROM.")
        while emu.getsystemid() == "NULL" do
            emu.frameadvance()
        end
    end
    
    rom_hash = gameinfo.getromhash()

    print("Waiting for client to connect. Emulation will freeze intermittently until a client is found.\n")

    local co = coroutine.create(main)
    function tick ()
        local status, err = coroutine.resume(co)
    
        if not status then
            print("\nERROR: "..err)
            print("Consider reporting this crash.\n")
    
            if server ~= nil then
                server:close()
            end
    
            co = coroutine.create(main)
        end
    end
    
    -- Gambatte has a setting which can cause script execution to become
    -- misaligned, so for GB and GBC we explicitly set the callback on
    -- vblank instead.
    -- https://github.com/TASEmulators/BizHawk/issues/3711
    if emu.getsystemid() == "GB" or emu.getsystemid() == "GBC" then
        event.onmemoryexecute(tick, 0x40, "tick", "System Bus")
    else
        event.onframeend(tick)
    end
    
    while true do
        emu.frameadvance()
    end
end
