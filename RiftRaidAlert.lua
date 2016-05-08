local function Pagura_Golems_Target_Name()
    local Crustok = Inspect.Unit.Castbar("u2B75B2CB73ED8E64")
    if Crustok ~= nil then
        if Crustok.abilityName == "Pain Bringer" then
            local Crustok_target = Inspect.Unit.Detail("u2B75B2CB73ED8E64.target")
            if Crustok_target ~= nil then
                print ("Crustok -> target -> "..Crustok_target.name)
            end
        end
    end
    local Brachy = Inspect.Unit.Castbar("u50D54CD171D9D26A")
    if Brachy ~= nil then
        if Brachy.abilityName == "Pain Bringer" then
            local Brachy_target = Inspect.Unit.Detail("u50D54CD171D9D26A.target")
            if Brachy_target ~= nil then
                print ("Brachy -> target -> "..Brachy_target.name)
            end
        end
    end
end


local function getAbilityName(event, units)
    if units then
        for id,value in pairs(units) do
            local details = Inspect.Unit.Detail(id)
            local cast = Inspect.Unit.Castbar(id)
            if value then
                if details.player == nil then
                    print(details.name.." -> "..cast.abilityName)
                end
            end
        end
    end
    Pagura_Golems_Target_Name()
end


local function getRemoveBuffName(event, unit, buffs)
    if unit then
        local details = Inspect.Unit.Detail(unit)
        for buffid, typeid in pairs(buffs) do
            local buff = Inspect.Buff.Detail(unit, buffid)
            for key, value in pairs(rra_bufflist) do
                if value.id == buffid then
                    print(value.name.." -> remove -> "..details.name)
                    table.remove(rra_bufflist,key)
                end
            end
        end
    end
end


local function getAddBuffName(event, unit, buffs)
    if unit then
        local details = Inspect.Unit.Detail(unit)
        for buffid, typeid in pairs(buffs) do
            local buff = Inspect.Buff.Detail(unit, buffid)
            if details.player then
                if details.id ~= buff.caster then
                    if buff.curse or buff.debuff or buff.disase then
                        print(buff.name.." -> "..details.name)
                        local bufflist = {id=buffid, name=buff.name}
                        table.insert (rra_bufflist,bufflist)
                    end
                end
            else
                if details.id == buff.caster then
                    print(buff.name.." -> "..details.name)
                    local bufflist = {id=buffid, name=buff.name}
                    table.insert (rra_bufflist,bufflist)
                end
            end
        end
    end
end


local function CombatBegin()
    local details = Inspect.Unit.Detail("player.target")
    if details ~= nil then
        print ("Combat Begin -> "..details.name)
    else
        print ("Combat Begin")
    end
end

local function CombatEnd()
    print ("Combat End")
end

local function rra_start()
    print ("Rift Raid Alert started")
    Command.Event.Attach(Event.Unit.Castbar, getAbilityName, "AbilityName")
    Command.Event.Attach(Event.Buff.Remove, getRemoveBuffName, "buffremoveevent")
    Command.Event.Attach(Event.Buff.Add, getAddBuffName, "buffaddevent")
    Command.Event.Attach(Event.System.Secure.Enter, CombatBegin,"Combat Begin")
    Command.Event.Attach(Event.System.Secure.Leave, CombatEnd,"Combat End")
end


local function rra_stop()
    print ("Rift Raid Alert stoped")
    Command.Event.Detach(Event.Unit.Castbar, getAbilityName, "AbilityName")
end


function slashHandler(h, args)
    local r = {}
    local numargs = 0
    for token in string.gmatch(args, "[^%s]+") do
        r[numargs] = token
        numargs=numargs+1
    end
    if r[0] == "start" then
        rra_start()
        return
    end
    if r[0] == "stop" then
        rra_stop()
        return
    end
    print ("/rra start - Rift Raid Alert start")
    print ("/rra stop - Rift Raid Alert stop")
end

rra_bufflist = {}
print("/rra - for a list of commands")
Command.Event.Attach(Command.Slash.Register("rra"), slashHandler, "Command.Slash.Register")