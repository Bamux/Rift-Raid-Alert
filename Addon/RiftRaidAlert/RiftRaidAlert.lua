local function Pagura_Golems_Target_Name()
    local Crustok = Inspect.Unit.Castbar("u2B75B2CB73ED8E64")
    if Crustok ~= nil then
        if Crustok.abilityName == "Pain Bringer" then
            local Crustok_target = Inspect.Unit.Detail("u2B75B2CB73ED8E64.target")
            if Crustok_target ~= nil then
                print ("Crustok Target = "..Crustok_target.name)
            end
        end
    end
    local Brachy = Inspect.Unit.Castbar("u50D54CD171D9D26A")
    if Brachy ~= nil then
        if Brachy.abilityName == "Pain Bringer" then
            local Brachy_target = Inspect.Unit.Detail("u50D54CD171D9D26A.target")
            if Brachy_target ~= nil then
                print ("Brachy Target = "..Brachy_target.name)
            end
        end
    end
end


local function getAbilityName()
    local cast = Inspect.Unit.Castbar("player.target")
    local target = Inspect.Unit.Detail("player.target")
	if cast ~= nil and target ~= nil then
	    print("Target = "..target.name..", ability = "..cast.abilityName)
    end
    Pagura_Golems_Target_Name()
end


local function rra_start()
	print ("Rift Raid Alert started")
        Command.Event.Attach(Event.Unit.Castbar, getAbilityName, "AbilityName")
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

print("/rra - for a list of commands")
Command.Event.Attach(Command.Slash.Register("rra"), slashHandler, "Command.Slash.Register")
