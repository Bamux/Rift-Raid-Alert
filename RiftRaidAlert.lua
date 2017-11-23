local rra_boss_id = 0
local rra_bufflist = {}
local Lavafield = Inspect.Time.Frame()
local Orchester = Inspect.Time.Frame()
local maxhitpoints = 0
local lasthitpoints = 100
local language = Inspect.System.Language()
local user_combat = false
print("language = " .. language)
-- local User = Inspect.Unit.Lookup("player")


local function CombatEnd()
    if rra_boss_id ~= 0 then
        print("Combat End")
        local count = #rra_bufflist
        for i=0, count do rra_bufflist[i]=nil end
        maxhitpoints = 0
        lasthitpoints = 100
        rra_boss_id = 0
    end
end


local function CombatCheck(event, units) -- Check Combat Status (Combat Begin, Combat End)
    if rra_boss_id == 0  then
        local hitpoints = 20000000
        local unit_details = Inspect.Unit.Detail(units)
        if unit_details then
            for id, detail in pairs(unit_details) do
                -- if not detail.relation then
                if detail.relation == "hostile" then
                    if tonumber(detail.level) then
                        if tonumber(detail.level) > 68 then
                            local hitpoints = 100000000
                        end
                    end
                    if detail.healthMax > hitpoints and detail.healthMax > maxhitpoints and detail.health > detail.healthMax*0.98 then
--                        if detail.id ~= "u800000024E02FC39" and detail.id ~= "u800000024E02FC3D" then
                            maxhitpoints = detail.healthMax
                            print("Combat Begin > ".. detail.name)
                            rra_boss_id = detail.id
                            local player = Inspect.Unit.Detail(detail.id .. ".target")
                            if player then
                                if player.role == "tank" then
                                    print("Tank pull >> " .. player.name)
                                else
                                    print("Fail pull >> " .. player.name)
                                end
                            end
--                        end
                    end
                end
            end
        end
    end
end


local function CombatChange(event, units)
    CombatCheck(event, units)
    local unit_details = Inspect.Unit.Detail(units)
    if unit_details and rra_boss_id ~= "0" and user_combat == false then
        for id, detail in pairs(unit_details) do
            if id == rra_boss_id  and not detail.combat then
                CombatEnd()
            end
        end
    end
end


local function CombatEnter(Input)
	user_combat = true
end


local function CombatExit(Input)
	user_combat = false
end


local function CombatDeath(event, unit)
    if unit.target then
        if unit.target == rra_boss_id then
            if unit.targetName then
                print("Boss Death > ".. unit.targetName)
            end
            CombatEnd()
        else
            if unit.targetName then
                local unit_detail = Inspect.Unit.Detail(unit.target)
                if unit_detail.player then
                    print("Death >> ".. unit.targetName)
                else
                    print("Death > ".. unit.targetName)
                end
            end
        end
    end
end


local function CheckHP(event, units)
    local unit_details = Inspect.Unit.Detail(units)
    local hitpoints = 100
    if  unit_details then
        for id, detail in pairs(unit_details) do
            if detail.id == rra_boss_id then
                local hitpoints_percent = detail.health*100/detail.healthMax
                while hitpoints >= 0 do
                    if  hitpoints_percent <= hitpoints and hitpoints_percent > hitpoints-1 then
                        if hitpoints ~= lasthitpoints then
                            print(detail.name .. " = " .. hitpoints .. " %")
                            lasthitpoints = hitpoints
--                            if hitpoints == 0 then -- or hitpoints == 100
--                                CombatEnd()
--                            end
                        end
                        break
                    end
                    hitpoints = hitpoints - 1
                end
            end
        end
    end
end


-- print Debuffs on all Player's (Player <  NPC) and Buffs on all NPC's (NPC < Buff)
local function getAddBuffName(event, unit, buffs)
    if unit then
        local details = Inspect.Unit.Detail(unit)
        if details then
            for buffid, typeid in pairs(buffs) do
                local buff = Inspect.Buff.Detail(unit, buffid)
                local target = Inspect.Unit.Detail(buff.caster)
                if buff then
                    if details.player then
                        if buff.type == "B14A2E6D609F79153" then -- Lavafield
                            if (Inspect.Time.Frame() - Lavafield) > 10 then
                                print("Rift Raid Alert > Lavafield")
                                Lavafield = Inspect.Time.Frame()
                            end
                        elseif buff.type == "BFD9F4FF8303ACEE6" or buff.type == "B39FB71DBD14135BE" then -- Orchester
                            if (Inspect.Time.Frame() - Orchester) > 15 then
                                print("Rift Raid Alert > Orchester")
                                Orchester = Inspect.Time.Frame()
                            end
                        end
                        if buff.name == "Anchored in Flames" or buff.name == "In Flammen verankert" or buff.name == "Ancrage de flammes" then -- Anchored in Flames "B44E44A80755620C3"
                            print(details.name .. " << " .. buff.name)
                        end
                        if details.id ~= buff.caster then
                            if target then
                                if target.player == nil and target.relation == "hostile" then
                                    if buff.description then
                                        print(details.name .. " << " ..buff.name .. " (" .. buff.description .. ")")
                                    else
                                        print(details.name .. " << " ..buff.name)
                                    end
                                    local bufflist = { id = buffid, name = buff.name }
                                    table.insert(rra_bufflist, bufflist)
                                end
                            end
                        end
                    else
                      if details.id == buff.caster and details.relation == "hostile" then
                            if buff.description then
                                print(details.name .. " < " .. buff.name .. " (" .. buff.description .. ")")
                            else
                                print(details.name .. " < " .. buff.name)
                            end
                            local bufflist = { id = buffid, name = buff.name }
                            table.insert(rra_bufflist, bufflist)
                        end
                    end
                end
            end
        end
    end
end


local function rra_raidbuffcheck()
    local groupmember = ""
    local names = ""
    local names_count = 0

    for i=1, 20 do
        local flask = false
        local weaponstone = false
        local food = false
        local groupmember = string.format("group%02d", i)
        local player = Inspect.Unit.Detail(groupmember)
--        if not player and i == 1 then
--            groupmember = "player"
--            player = Inspect.Unit.Detail(groupmember)
--        end
        local buffs = Inspect.Buff.List(groupmember)
        if buffs and player.role ~= "tank" then
            for buffid, typeid in pairs(buffs) do
                local detail = Inspect.Buff.Detail(groupmember, buffid)
                if detail and player then
                    if detail.rune then
                        if player.calling == "mage" or player.calling == "cleric" then
                            if detail.rune == "r143A1D7A79A201D6" then -- Faetouched Powerstone = r143A1D7A79A201D6
                                if detail.remaining > 300 then
                                    weaponstone = true
                                end
                            end
                        else
                            if detail.rune == "rFA65F5184E42C822" or detail.rune == "r70B0A3843EC153B8" then -- Atramentium Whetstone = rFA65F5184E42C822, Atramentium Oilstone = r70B0A3843EC153B8
                                if detail.remaining > 300 then
                                    weaponstone = true
                                end
                            end
                        end
                    end
                    if detail.type then
                        if player.calling == "mage" or player.calling == "cleric" then
                            if detail.type == "B76F46FAA030D4A53" or detail.type == "B599B39124D958B4F" then --  Visionary Brightsurge Vial = B76F46FAA030D4A53, Prophetic Brightsurge Vial = B599B39124D958B4F
                                if detail.remaining > 300 then
                                    flask = true
                                end
                            end
                            if detail.type == "B40C3D8E1646C6DD1" then --  Gedlo Curry Pot (SP) = B40C3D8E2646C6DD1
                                if detail.remaining > 300 then
                                    food = true
                                end
                            end
                        else
                            if detail.type == "B6A8C5F8010D4EFBB" or detail.type == "B03ABEAB575CC9A8E" then --  Visionary Powersurge Vial = B6A8C5F8110D4EFBB, Prophetic Powersurge Vial = B03ABEAB575CC9A8E
                                if detail.remaining > 300 then
                                    flask = true
                                end
                            end
                            if detail.type == "B40C3D8E33D686C51" then --  Gedlo Curry Pot (AP) = B40C3D8E43D686C51
                                if detail.remaining > 300 then
                                    food = true
                                end
                            end
                        end
                    end
                end
            end

            local playersplit = ""
            if weaponstone == false or flask == false  or food == false then
                names_count = names_count + 1
                for x in string.gmatch(player.name, '([^@]+)') do
                    playersplit = x
                    break
                end
                if names_count > 1 then
                    playersplit = ", " .. playersplit
                end
                names = names .. playersplit

            end
        end
    end
    if names ~= "" then
        print ("Raidbuffs missing: " .. names_count .. " players > " .. names)
        print()
    end
end


local function test()
    local buffs = Inspect.Buff.List("player.target")
    for buffid, typeid in pairs(buffs) do
        local detail = Inspect.Buff.Detail("player.target", buffid)
        --dump (detail)
        if detail then
            if detail.rune then
                if detail.description then
                    print(detail.name .. " detail.rune = " .. detail.rune .. " detail.id = " .. detail.id .. " detail.description = " .. detail.description)
                else
                    print(detail.name .. " detail.rune = " .. detail.rune .. " detail.id = " .. detail.id)
                end
            end
            if detail.type then
                if detail.description then
                    print(detail.name .. " detail.type = " .. detail.type .. " detail.id = " .. detail.id .. " detail.description = " .. detail.description)
                else
                    print(detail.name .. " detail.rune = " .. detail.rune .. " detail.id = " .. detail.id)
                end
            end
        end
    end
end


-- print all removed Debuffs (Player <  remove Debuff)  and Buffs (NPC < remove Buff)
local function getRemoveBuffName(event, unit, buffs)
    if unit then
        local buff_existing = false
        local details = Inspect.Unit.Detail(unit)
        if details then
            for buffid, typeid in pairs(buffs) do
                for key, value in pairs(rra_bufflist) do
                    if value.id == buffid then
                        local buff_list = Inspect.Buff.List(unit)
                        local buff_details = Inspect.Buff.Detail(unit,buff_list)
                        if buff_list then
                            for k, v in pairs(buff_details) do
                               if v.name == value.name then
                                   buff_existing = true
                               end
                            end
                        end
                        if buff_existing == false then
                            if details.player then
                                print(details.name .. " << remove " .. value.name)
                            else
                                print(details.name .. " < remove " .. value.name)
                            end
                        end
                        table.remove(rra_bufflist, key)
                    end
                end
            end
        end
    end
end


-- print all Abilities (with cast time) from NPC's and show their target (NPC > Ability > Target)
local function getAbilityName(event, units)
    local unit_details = Inspect.Unit.Detail(units)
    if unit_details then
        for id, detail in pairs(unit_details) do
            local cast = Inspect.Unit.Castbar(id)
            if cast then
                if detail.relation == "hostile" then
                    local player = Inspect.Unit.Detail(id..".target")
                    if player then
                        if cast.abilityNew then
                            local ability_detail = Inspect.Ability.New.Detail(cast.abilityNew)
                            if ability_detail.description ~= nil then
                                print (detail.name .. " > " .. cast.abilityName.. " >> " .. player.name  .. " (" .. ability_detail.description .. ")")
                            else
                                print (detail.name .. " > " .. cast.abilityName.. " >> " .. player.name)
                            end
                        else
                            print (detail.name .. " > " .. cast.abilityName.. " >> " .. player.name)
                        end
                    else
                        if cast.abilityNew then
                            local ability_detail = Inspect.Ability.New.Detail(cast.abilityNew)
                            if ability_detail.description ~= nil then
                                print(detail.name .. " > " .. cast.abilityName  .. " (" .. ability_detail.description .. ")")
                            else
                                print(detail.name .. " > " .. cast.abilityName)
                            end
                        else
                            print(detail.name .. " > " .. cast.abilityName)
                        end
                    end
                else
                    if cast.abilityNew then
                        if cast.abilityNew == "A24FE01816BA3C9E7" then -- Call of the Ascended (Raid rez)
                            CombatEnd()
                            return
                        end
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
        if zone then
            if zone.name then
                print("Rift Raid Alert Trigger > ".. zone.name)
            end
        end
    end
end


local function ReadyCheck(event, units)
    local unit_details = Inspect.Unit.Detail(units)
    local player = Inspect.Unit.Detail("player")
    if unit_details and player then
        for id, detail in pairs(unit_details) do
            if detail.id == player.id then
                if detail.ready then
                    print("language = " .. language)
                    CombatEnd()
                    Zone()
                    print("player >> " .. player.name)
                    rra_raidbuffcheck()
                end
            end
        end
    end
end


local function rra_stop()
    Command.Event.Detach(Event.Unit.Detail.Combat, CombatChange, "CombatCheck")
    Command.Event.Detach(Event.Combat.Death, CombatDeath, "CombatDeathCheck")
    Command.Event.Detach(Event.Unit.Detail.Ready, ReadyCheck, "ReadyCheck")
    Command.Event.Detach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Detach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Detach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    Command.Event.Detach(Event.Unit.Detail.Health, CheckHP, "CheckHP")
	Command.Event.Detach(Event.Combat.Damage, Damage, "Damage")
	Command.Event.Detach(Event.System.Secure.Enter, CombatEnter, "Enter")
	Command.Event.Detach(Event.System.Secure.Leave, CombatExit, "Exit")
    --Command.Event.Detach(Event.Chat.Notif, ScreenNotification, "ScreenNotification")
    --Command.Event.Detach(Event.Unit.Detail.Zone, ChangeZone, "ChangeZone")
end


local function rra_start()
    rra_stop()
--	Command.Event.Attach(Event.Combat.Damage, Damage, "Damage")
    Command.Event.Attach(Event.Unit.Detail.Combat, CombatChange, "CombatCheck")
    Command.Event.Attach(Event.Combat.Death, CombatDeath, "CombatDeathCheck")
    Command.Event.Attach(Event.Unit.Detail.Ready, ReadyCheck, "ReadyCheck")
    Command.Event.Attach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Attach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Attach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    Command.Event.Attach(Event.Unit.Detail.Health, CheckHP, "CheckHP")
	Command.Event.Attach(Event.System.Secure.Enter, CombatEnter, "CombatEnter")
	Command.Event.Attach(Event.System.Secure.Leave, CombatExit, "CombatExit")
    --Command.Event.Attach(Event.Chat.Notif, ScreenNotification, "ScreenNotification")
    --Command.Event.Attach(Event.Unit.Detail.Zone, ChangeZone, "ChangeZone")
end


local function start_check(addon)
    print("/rra - for a list of commands")
    if RiftRaidAlert_enabled then
        if RiftRaidAlert_enabled == "start" then
            rra_start()
        elseif RiftRaidAlert_enabled == "keywords" then
            print("Rift Raid Alert Trigger > keywords")
        end
    end
end


local function id()
    local target = Inspect.Unit.Detail("player.target")
        if target then
            print(target.name .. " > UnitID: " .. target.id)
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
            print("Rift Raid Alert Trigger < keywords off")
        else
           print("Rift Raid Alert stoped")
        end
        RiftRaidAlert_enabled = nil
        rra_stop()
        return
    end
    if r[0] == "start" then
        print("language = " .. language)
        if RiftRaidAlert_enabled == "keywords" then
            print("Rift Raid Alert Trigger < keywords off")
        end
        RiftRaidAlert_enabled = "start"
        print("Rift Raid Alert started")
        rra_start()
        Zone()
        return
    end
    if r[0] == "keywords" then
        print("language = " .. language)
        if RiftRaidAlert_enabled == "start" then
            print("Rift Raid Alert stoped")
        end
        RiftRaidAlert_enabled = "keywords"
        print("Rift Raid Alert Trigger > Keywords on")
        rra_stop()
        return
    end
    if r[0] == "check" then
        print("language = " .. language)
        local player = Inspect.Unit.Detail("player")
        print("player >> " .. player.name)
        rra_raidbuffcheck()
        return
    end
    if r[0] == "target" then
        print("Target Check")
        test()
        return
    end
        if r[0] == "id" then
        print("id")
        id()
        return
    end
    print("/rra start - start Raid announcements for RoF, IGP, MoM and CoA")
    print("/rra stop - stop Rift Raid Alert")
    print("/rra keywords - search the chat for keywords from your keywords.txt")
    print("/rra check - checks waeponstones, flasks and foodof all players in the raid")
end

Command.Event.Attach(Event.Addon.Startup.End, start_check, "StartCheck")
Command.Event.Attach(Command.Slash.Register("rra"), slashHandler, "Command.Slash.Register")

