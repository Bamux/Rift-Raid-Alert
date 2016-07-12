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
            if detail.id == rra_boss_id and detail.health < 1 then
                print("Combat End -> ".. detail.name)
                local count = #rra_bufflist
                for i=0, count do rra_bufflist[i]=nil end
                rra_boss_id = nil
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


local function rra_raidbuffcheck()
    print("Buff Check")
    local weaponstones_flasks_food = {}
    local weaponstones_flasks = {}
    local weaponstones_food = {}
    local flasks_food = {}
    local weaponstones = {}
    local flasks = {}
    local foods = {}
    local count = 0
    local groupmember = ""

    for i=1, 20 do
        local flask = false
        local weaponstone = false
        local food = false
        local groupmember = string.format("group%02d", i)
        local player = Inspect.Unit.Detail(groupmember)
        local buffs = Inspect.Buff.List(groupmember)
        if buffs and player.role ~= "tank" then
            for buffid, typeid in pairs(buffs) do
                local detail = Inspect.Buff.Detail(groupmember, buffid)
                if detail and player then
                    if detail.rune then
                        if player.calling == "mage" or player.calling == "cleric" then
                            if detail.rune == "r54A72A7D7486A939" then -- Pelagic Powerstone = r54A72A7D7486A939
                                if detail.duration > 300 then
                                    weaponstone = true
                                end
                            end
                        else
                            if detail.rune == "r762BD1423747FA3F" or detail.rune == "r0C2445386997ECE6" then -- Coral Oilstone = r762BD1423747FA3F, Coral Whetstone = r0C2445386997ECE6
                                if detail.duration > 300 then
                                    weaponstone = true
                                end
                            end
                        end
                    end
                    if detail.type then
                        if player.calling == "mage" or player.calling == "cleric" then
                            if detail.type == "B5FB47C7B1CE019F8" or detail.type == "B2A1357781A34EE07" then --  Illustrious Brightsurge Vial = B5FB47C7B1CE019F8, Phenomenal Brightsurge Vial = B2A1357781A34EE07
                                if detail.duration > 300 then
                                    flask = true
                                end
                            end
                            if detail.type == "B3CA755DE889572AE" then --  Feast of the Rhenke (SP) = B3CA755DE889572AE
                                if detail.duration > 300 then
                                    food = true
                                end
                            end
                        else
                            if detail.type == "B45441A66942B2875" or detail.type == "B4E57169B18162520" then --  Illustrious Powersurge Vial = B45441A66942B2875, Phenomenal Powersurge Vial = B4E57169B18162520
                                if detail.duration > 300 then
                                    flask = true
                                end
                            end
                            if detail.type == "B3CA755E06191712E" then --  Feast of the Rhenke (AP) = B3CA755E06191712E
                                if detail.duration > 300 then
                                    food = true
                                end
                            end
                        end
                    end
                end
            end
            if weaponstone == false and flask == false  and food == false then
                table.insert(weaponstones_flasks_food, player.name)
                count = count + 1
            elseif weaponstone == false and flask == false then
                table.insert(weaponstones_flasks, player.name)
                count = count + 1
            elseif weaponstone == false and food == false then
                table.insert(weaponstones_food, player.name)
                count = count + 1
            elseif flask == false and food == false then
                table.insert(flasks_food, player.name)
                count = count + 1
            elseif weaponstone == false then
                table.insert(weaponstones, player.name)
                count = count + 1
            elseif flask == false then
                table.insert(flasks, player.name)
                count = count + 1
            elseif food == false then
                table.insert(foods, player.name)
                count = count + 1
            end
        end
    end

    if count > 0 and count <= 4 then
        local buff_count = #weaponstones_flasks_food
        if buff_count > 0 then
            for i=1, buff_count do
                print("Raidbuff missing -> " .. weaponstones_flasks_food[i])
            end
            print("Raidbuff missing <--- Weaponstone, Flask and Food")
        end
        buff_count = #weaponstones_flasks
        if buff_count > 0 then
            for i=1, buff_count do
                print("Raidbuff missing -> " .. weaponstones_flasks[i])
            end
            print("Raidbuff missing <-- Weaponstone and Flask")
        end
        buff_count = #weaponstones_food
        if buff_count > 0 then
            for i=1, buff_count do
                print("Raidbuff missing -> " .. weaponstones_food[i])
            end
            print("Raidbuff missing <-- Weaponstone and Food")
        end
        buff_count = #flasks_food
        if buff_count > 0 then
            for i=1, buff_count do
                print("Raidbuff missing -> " .. flasks_food[i])
            end
            print("Raidbuff missing <-- Flask and Food")
        end
        buff_count = #weaponstones
        if buff_count > 0 then
            for i=1, buff_count do
                print("Raidbuff missing -> " .. weaponstones[i])
            end
            print("Raidbuff missing <- Weaponstone")
        end
        local buff_count = #flasks
        if buff_count > 0 then
            for i=1, buff_count do
                print("Raidbuff missing -> " .. flasks[i])
            end
            print("Raidbuff missing <- Flask")
        end
        local buff_count = #foods
        if buff_count > 0 then
            for i=1, buff_count do
                print("Raidbuff missing -> " .. foods[i])
            end
            print("Raidbuff missing <- Food")
        end
    elseif count > 4 then
        print("Raidbuff missing -> " .. count)
        print("Raidbuff missing number <- Weaponstone, Flask or Food")
    end
end


local function test()
    local buffs = Inspect.Buff.List("player.target")
    for buffid, typeid in pairs(buffs) do
        local detail = Inspect.Buff.Detail("player.target", buffid)
        --dump (detail)
        if detail then
            if detail.rune then
                print(detail.name .. " = " .. detail.rune)
            end
            if detail.type then
                print(detail.name .. " = " .. detail.type)
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


local function Zone()
    local detail = Inspect.Unit.Detail("player")
    if detail then
        local zone_id = detail.zone
        local zone = Inspect.Zone.Detail(zone_id)
        if zone.name then
            print("Rift Raid Alert Trigger -> ".. zone.name)
        end
    end
end


local function ReadyCheck(event, units)
    local unit_details = Inspect.Unit.Detail(units)
    local player = Inspect.Unit.Detail("player")
    for id, detail in pairs(unit_details) do
        if detail.id == player.id then
            if detail.ready then
                CombatEnd()
                Zone()
                rra_raidbuffcheck()
            end
        end
    end
end


local function rra_stop()
    Command.Event.Detach(Event.Unit.Detail.Combat, CombatCheck, "CombatCheck")
    Command.Event.Detach(Event.Combat.Death, CombatDeath, "CombatDeathCheck")
    Command.Event.Detach(Event.Unit.Detail.Ready, ReadyCheck, "ReadyCheck")
    Command.Event.Detach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Detach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Detach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    --Command.Event.Detach(Event.Unit.Detail.Zone, ChangeZone, "ChangeZone")
end


local function rra_start()
    rra_stop()
    Command.Event.Attach(Event.Unit.Detail.Combat, CombatCheck, "CombatCheck")
    Command.Event.Attach(Event.Combat.Death, CombatDeath, "CombatDeathCheck")
    Command.Event.Attach(Event.Unit.Detail.Ready, ReadyCheck, "ReadyCheck")
    Command.Event.Attach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Attach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Attach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    --Command.Event.Attach(Event.Unit.Detail.Zone, ChangeZone, "ChangeZone")
    print("Rift Raid Alert started")
end


local function start_check(addon)
    print("/rra - for a list of commands")
    if RiftRaidAlert_enabled then
        if RiftRaidAlert_enabled == "start" then
            rra_start()
        elseif RiftRaidAlert_enabled == "keywords" then
            print("Rift Raid Alert Trigger -> keywords")
        end
    end
end


local function slashHandler(h, args)
    local r = {}
    local numargs = 0
    for token in string.gmatch(args, "[^%s]+") do
        r[numargs] = token
        numargs = numargs + 1
    end
    if r[0] == "stop" then
        if RiftRaidAlert_enabled == "keywords" then
            print("Rift Raid Alert Trigger <- keywords off")
        else
           print("Rift Raid Alert stoped")
        end
        RiftRaidAlert_enabled = nil
        rra_stop()
        return
    end
    if r[0] == "start" then
        if RiftRaidAlert_enabled == "keywords" then
            print("Rift Raid Alert Trigger <- keywords off")
        end
        RiftRaidAlert_enabled = "start"
        rra_start()
        Zone()
        return
    end
    if r[0] == "keywords" then
        if RiftRaidAlert_enabled == "start" then
            print("Rift Raid Alert stoped")
        end
        RiftRaidAlert_enabled = "keywords"
        print("Rift Raid Alert Trigger -> Keywords on")
        rra_stop()
        return
    end
    if r[0] == "check" then
        rra_raidbuffcheck()
        return
    end
    if r[0] == "target" then
        print("Target Check")
        test()
        return
    end
    print("/rra start - Rift Raid Alert start")
    print("/rra stop - Rift Raid Alert stop")
    print("/rra keywords - search the chat for keywords")
end

Command.Event.Attach(Event.Addon.Startup.End, start_check, "StartCheck")
Command.Event.Attach(Command.Slash.Register("rra"), slashHandler, "Command.Slash.Register")
