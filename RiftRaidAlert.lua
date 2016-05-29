
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


local function CombatChange()
    if rra_combatbegin == "out_of_combat" then
        local inspect = Inspect.Unit.Detail
        local list = Inspect.Unit.List()
        local format = tostring
        for k,v in pairs(list) do
            local detail = inspect(format(k))
            if detail and detail.relation == "hostile" and detail.health > detail.healthMax*0.98 then
                print("! Combat Begin -> ".. detail.name)
                rra_combatbegin = detail.id
            end
        end
    end
end


local function CombatEnd()
    print("Combat End")
    local count = #rra_bufflist
    for i=0, count do rra_bufflist[i]=nil end
    rra_combatbegin = "out_of_combat"
    rra_health = 100
end


local function CombatBegin()
    if rra_combatbegin == "out_of_combat" then
        local details = Inspect.Unit.Detail("player.target")
        if details ~= nil then
            rra_combatbegin = details.id
            print("Combat Begin -> " .. details.name)
        else
            print("Combat Begin")
        end
    end
end

-- print the Hitpoints from the first NPC with agro
local function CheckHP(units)
    if rra_combatbegin ~= "out_of_combat" then
        local detail = Inspect.Unit.Detail(rra_combatbegin)
        if detail ~= nil then
            local percent = (100/detail.healthMax*detail.health)
            if percent == 100 then
                print(detail.name .. " -> " .. "100 %")
                rra_health = 100
                CombatEnd()
            elseif percent <= 90 and  percent > 80 then
                if rra_health ~= 90 then
                    print(detail.name .. " -> " .. "90 %")
                    rra_health = 90
                end
            elseif percent <= 80 and  percent > 70 then
                if rra_health ~= 80 then
                    print(detail.name .. " -> " .. "80 %")
                    rra_health = 80
                end
            elseif percent <= 70 and  percent > 60 then
                if rra_health ~= 70 then
                    print(detail.name .. " -> " .. "70 %")
                    rra_health = 70
                end
            elseif percent <= 60 and  percent > 50 then
                if rra_health ~= 60 then
                    print(detail.name .. " -> " .. "60 %")
                    rra_health = 60
                end
            elseif percent <= 50 and  percent > 40 then
                if rra_health ~= 50 then
                    print(detail.name .. " -> " .. "50 %")
                    rra_health = 50
                end
            elseif percent <= 40 and  percent > 30 then
                if rra_health ~= 40 then
                    print(detail.name .. " -> " .. "40 %")
                end
                rra_health = 40
            elseif percent <= 30 and  percent > 20 then
                if rra_health ~= 30 then
                    print(detail.name .. " -> " .. "30 %")
                end
                rra_health = 30
            elseif percent <= 20 and  percent > 10 then
                if rra_health ~= 20 then
                    print(detail.name .. " -> " .. "20 %")
                end
                rra_health = 20
            elseif percent <= 10 and  percent > 0 then
                if rra_health ~= 10 then
                    print(detail.name .. " -> " .. "10 %")
                end
                rra_health = 10
            elseif percent == 0 then
                print(detail.name .. " -> " .. "0 %")
                CombatEnd()
            end
        end
    end
end


local function rra_stop()
    Command.Event.Detach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Detach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Detach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    Command.Event.Attach(Event.Unit.Detail.Combat, CombatChange, "CombatChange")
    Command.Event.Detach(Event.System.Secure.Enter, CombatBegin, "CombatBegin")
    Command.Event.Detach(Event.System.Secure.Leave, CombatEnd, "CombatEnd")
    Command.Event.Detach(Event.Unit.Detail.Health, CheckHP, "CheckHP")
end


local function rra_start()
    rra_stop()
    Command.Event.Attach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Attach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Attach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    Command.Event.Attach(Event.Unit.Detail.Combat, CombatChange, "CombatChange")
    Command.Event.Attach(Event.System.Secure.Enter, CombatBegin, "CombatBegin")
    Command.Event.Attach(Event.System.Secure.Leave, CombatEnd, "CombatEnd")
    Command.Event.Attach(Event.Unit.Detail.Health, CheckHP, "CheckHP")
end


local function slashHandler(h, args)
    local r = {}
    local numargs = 0
    for token in string.gmatch(args, "[^%s]+") do
        r[numargs] = token
        numargs = numargs + 1
    end
    if r[0] == "start" then
        print("Rift Raid Alert started")
        rra_start()
        return
    end
    if r[0] == "stop" then
        print("Rift Raid Alert stoped")
        rra_stop()
        return
    end
    print("/rra start - Rift Raid Alert start")
    print("/rra stop - Rift Raid Alert stop")
end

rra_bufflist = {}
rra_combatbegin = "out_of_combat"
rra_health = 100
print("/rra - for a list of commands")
Command.Event.Attach(Command.Slash.Register("rra"), slashHandler, "Command.Slash.Register")
