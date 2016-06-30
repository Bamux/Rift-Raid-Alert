local rra_boss_id
local rra_bufflist = {}


local function CombatEnd()
    if rra_boss_id then
        print("Combat End")
        local count = #rra_bufflist
        for i=0, count do rra_bufflist[i]=nil end
        rra_boss_id = nil
    end
end


local function CombatCheck(event, units) -- Check Combat Status (Combat Begin, Combat End)
    if not rra_boss_id then
        local unit_details = Inspect.Unit.Detail(units)
        for id, detail in pairs(unit_details) do
            if detail.relation == "hostile" and detail.healthMax > 20000000 and detail.health > detail.healthMax*0.98 then
                print("Combat Begin -> ".. detail.name)
                rra_boss_id = detail.id
                break
            end
        end
    end
end


local function CombatDeath(event, units)
    if rra_boss_id then
        local unit_details = Inspect.Unit.Detail(units)
        for id, detail in pairs(unit_details) do
            if detail.id == rra_boss_id then
                print("Combat End -> ".. detail.name)
                local count = #rra_bufflist
                for i=0, count do rra_bufflist[i]=nil end
                rra_boss_id = nil
                break
            end
        end
    end
end

-- print Debuffs on all Player's (Player <-  NPC) and Buffs on all NPC's (NPC <- Buff)
local function getAddBuffName(event, unit, buffs)
    if unit then
        local details = Inspect.Unit.Detail(unit)
        for buffid, typeid in pairs(buffs) do
            local buff = Inspect.Buff.Detail(unit, buffid)
            local target = Inspect.Unit.Detail(buff.caster)
            if details.player ~= nil then
                if details.id ~= buff.caster then
                    if target ~= nil then
                        if target.player == nil then
                            if buff.curse or buff.debuff or buff.disase or buff.poison then
                                print(details.name .. " <- " ..buff.name)
                                local bufflist = { id = buffid, name = buff.name }
                                table.insert(rra_bufflist, bufflist)
                            end
                        end
                    end
                end
            else
                if details.id == buff.caster and details.relation == "hostile" then
                    print(details.name .. " <- " ..buff.name)
                    local bufflist = { id = buffid, name = buff.name }
                    table.insert(rra_bufflist, bufflist)
                end
            end
        end
    end
end


-- print all removed Debuffs (Player <-  remove Debuff)  and Buffs (NPC <- remove Buff)
local function getRemoveBuffName(event, unit, buffs)
    if unit then
        local buff_existing = false
        local details = Inspect.Unit.Detail(unit)
        for buffid, typeid in pairs(buffs) do
            for key, value in pairs(rra_bufflist) do
                if value.id == buffid then
                    local buff_list = Inspect.Buff.List(unit)
                    local buff_details = Inspect.Buff.Detail(unit,buff_list)
                    if buff_list ~= nill then
                        for k, v in pairs(buff_details) do
                           if v.name == value.name then
                               buff_existing = true
                           end
                        end
                    end
                    if buff_existing == false then
                        print(details.name .. " <- remove " .. value.name )
                    end
                    table.remove(rra_bufflist, key)
                end
            end
        end
    end
end


-- print all Abilities (with cast time) from NPC's and show their target (NPC -> Ability -> Target)
local function getAbilityName(event, units)
    if units then
        for id, value in pairs(units) do
            if value then
                local details = Inspect.Unit.Detail(id)
                local cast = Inspect.Unit.Castbar(id)
                if cast.abilityNew ~= nill then
                    if cast.abilityNew == "A24FE01816BA3C9E7" then -- Call of the Ascended (Raid rez)
                        CombatEnd()
                        return
                    end
                end
                if details.relation == "hostile" then
                    local target = Inspect.Unit.Detail(id..".target")
                    if target ~= nil then
                        print (details.name .. " -> " .. cast.abilityName.. " -> " .. target.name)
                    else
                        print(details.name .. " -> " .. cast.abilityName)
                    end
                end
            end
        end
    end
end


local function rra_stop()
    Command.Event.Detach(Event.Unit.Detail.Combat, CombatCheck, "CombatCheck")
    Command.Event.Detach(Event.Combat.Death, CombatDeath, "CombatDeathCheck")
    Command.Event.Detach(Event.Unit.Detail.Ready, CombatEnd, "CombatEnd")
    Command.Event.Detach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Detach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Detach(Event.Unit.Castbar, getAbilityName, "AbilityName")
end


local function rra_start()
    rra_stop()
    Command.Event.Attach(Event.Unit.Detail.Combat, CombatCheck, "CombatCheck")
    Command.Event.Attach(Event.Combat.Death, CombatDeath, "CombatDeathCheck")
    Command.Event.Attach(Event.Unit.Detail.Ready, CombatEnd, "CombatEnd")
    Command.Event.Attach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Attach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Attach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    print("Rift Raid Alert started")
end


local function start_check(addon)
    print("/rra - for a list of commands")
    if RiftRaidAlert_enabled then
        rra_start()
    end
end


local function slashHandler(h, args)
    local r = {}
    local numargs = 0
    for token in string.gmatch(args, "[^%s]+") do
        r[numargs] = token
        numargs = numargs + 1
    end
    if r[0] == "start" then
        RiftRaidAlert_enabled = true
        rra_start()
        return
    end
    if r[0] == "stop" then
        RiftRaidAlert_enabled = nil
        print("Rift Raid Alert stoped")
        rra_stop()
        return
    end
    print("/rra start - Rift Raid Alert start")
    print("/rra stop - Rift Raid Alert stop")
end


Command.Event.Attach(Event.Addon.Startup.End, start_check, "StartCheck")
Command.Event.Attach(Command.Slash.Register("rra"), slashHandler, "Command.Slash.Register")
