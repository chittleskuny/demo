function at()
end


function cron()
end


local function split_string(str, delimiter)
    if type(str) ~= 'string' or str == '' or type(delimiter) ~= 'string' or delimiter == '' then
        return nil
    end
    local string_list = {}
    for m in (str..delimiter).gmatch('(.-)'..delimiter) do
        if m and m ~= '' then
            local tmp = string.gsub(m, '^%s*(.-)%s*$', '%1')
            if tmp ~= '' then
                table.insert(string_list, tmp)
            end
        end
    end
    return string_list
end


local function format_pattern(pattern)
    local new_pattern = {}

    if type(pattern) == 'string' then
        local string_list = split_string(pattern, ' ')
        if #string_list == 5 then
            new_pattern = {
                minute       = string_list[1],
                hour         = string_list[2],
                day_of_month = string_list[3],
                month        = string_list[4],
                day_of_week  = string_list[5],
            }
        elseif #string_list == 6 then
            new_pattern = {
                minute       = string_list[1],
                hour         = string_list[2],
                day_of_month = string_list[3],
                month        = string_list[4],
                day_of_week  = string_list[5],
                year         = string_list[6],
            }
        elseif #string_list == 7 then
            new_pattern = {
                second       = string_list[1],
                minute       = string_list[2],
                hour         = string_list[3],
                day_of_month = string_list[4],
                month        = string_list[5],
                day_of_week  = string_list[6],
                year         = string_list[7],
            }
        else
            return nil
        end
    elseif type(pattern) == 'table' then
        new_pattern = pattern
    else
        return nil
    end

    if new_pattern.hour_minute_second then
        new_pattern.hour = ''
        new_pattern.minute = ''
        new_pattern.second = ''
    end

    return new_pattern
end


local function format_case(case)
    local new_case = case

    if type(case) == 'number' then
        if case >= 0 then
            new_case = {
                second = tonumber(os.date('%S', case)),
                minute = tonumber(os.date('%M', case)),
                hour   = tonumber(os.date('%H', case)),
                day    = tonumber(os.date('%d', case)),
                month  = tonumber(os.date('%m', case)),
                year   = tonumber(os.date('%Y', case)),
            }
        end
    elseif type(case) == 'string' then
        -- TODO
    elseif type(case) == 'table' then
        new_case = case
    end

    new_case.day_of_week = tonumber(os.date('*t', os.time({ year = new_case.year, month = new_case.month, day = new_case.day_of_month })).wday) - 1

    -- TODO
    new_case.day_of_trade = ''
    -- new_case.day_of_trade = '0'
    -- new_case.day_of_trade = '1'

    return new_case
end


local function match_second(pattern, case)
    if pattern.second == '' or pattern.second == '*' or pattern.second == '?' then
        return true
    end
    -- TODO
    return false
end


local function match_minute(pattern, case)
    if pattern.minute == '' or pattern.minute == '*' or pattern.minute == '?' then
        return true
    end
    -- TODO
    return false
end


local function match_hour(pattern, case)
    if pattern.hour == '' or pattern.hour == '*' or pattern.hour == '?' then
        return true
    end
    -- TODO
    return false
end


local function match_day_of_month(pattern, case)
    if pattern.day_of_month == '' or pattern.day_of_month == '*' or pattern.day_of_month == '?' then
        return true
    elseif string.match(pattern.day_of_month, '^[0-9]+$') then
        if tonumber(pattern.day_of_month) == case.day_of_month then
            return true
        end
    elseif string.match(pattern.day_of_month, '^([0-9]+),([0-9]+)[^/]*$') then
        local pattern_days = split_string(pattern.day_of_month, ',')
        for i_pattern_day, v_pattern_day in ipairs(pattern_days) do
            if tonumber(v_pattern_day) == case.day_of_month then
                return true
            end
        end
    elseif string.match(pattern.day_of_month, '^([0-9]+)%-([0-9]+)$') then
        local pattern_days = split_string(pattern.day_of_month, '-')
        if tonumber(pattern_days[1]) <= case.day_of_month and case.day_of_month <= tonumber(pattern_days[2]) then
            return true
        end
    elseif string.match(pattern.day_of_month, '^([0-9]+)%-([0-9]+)/([0-9]+)$') then
        local m = {}
        for i in pattern.day_of_month:gmatch('[0-9]+') do
            table.insert(m, i)
        end
        local start_time, end_time, step_time = tonumber(m[1]), tonumber(m[2]), tonumber(m[3])
        if start_time <= case.day_of_month and case.day_of_month <= end_time and math.fmod(case.day_of_month - start_time, step_time) == 0 then
            return true
        end
    else
        -- TODO
    end
    return false
end


local function match_month(pattern, case)
    if pattern.month == '' or pattern.month == '*' or pattern.month == '?' then
        return true
    elseif string.match(pattern.month, '^[0-9][012]*$') then
        if tonumber(pattern.month) == case.month then
            return true
        end
    elseif string.match(pattern.month, '^([0-9][012]*),([0-9][012]*)[^/]*$') then
        local pattern_months = split_string(pattern.month, ',')
        for i_pattern_month, v_pattern_month in ipairs(pattern_months) do
            if tonumber(v_pattern_month) == case.month then
                return true
            end
        end
    elseif string.match(pattern.month, '^([0-9][012]*)%-([0-9][012]*)$') then
        local pattern_months = split_string(pattern.month, '-')
        if tonumber(pattern_months[1]) <= case.month and case.month <= tonumber(pattern_months[2]) then
            return true
        end
    elseif string.match(pattern.month, '^([0-9][012]*)%-([0-9][012]*)/([0-9]+)$') then
        local m = {}
        for i in pattern.month:gmatch('[0-9]+') do
            table.insert(m, i)
        end
        local start_time, end_time, step_time = tonumber(m[1]), tonumber(m[2]), tonumber(m[3])
        if start_time <= case.month and case.month <= end_time and math.fmod(case.month - start_time, step_time) == 0 then
            return true
        end
    else
        -- TODO
    end
    return false
end


local function match_day_of_week(pattern, case)
    if pattern.day_of_week == '' or pattern.day_of_week == '*' or pattern.day_of_week == '?' then
        return true
    elseif string.match(pattern.day_of_week, '^[0-6]$') then
        if tonumber(pattern.day_of_week) == case.day_of_week then
            return true
        end
    elseif string.match(pattern.day_of_week, '^[0-6],[0-6][^/]*$') then
        local pattern_days = split_string(pattern.day_of_week, ',')
        for i_pattern_day, v_pattern_day in ipairs(pattern_days) do
            if tonumber(v_pattern_day) == tonumber(case.day_of_week) then
                return true
            end
        end
    elseif string.match(pattern.day_of_week, '[0-6]%-[0-6]$') then
        local pattern_days = split_string(pattern.day_of_week, '-')
        if tonumber(pattern_days[1]) <= case.day_of_week and case.day_of_week <= tonumber(pattern_days[2]) then
            return true
        end
    elseif string.match(pattern.day_of_week, '[0-6]%-[0-6]/[1-6]$') then
        local m = {}
        for i in pattern.day_of_week:gmatch('[0-6]+') do
            table.insert(m, i)
        end
        local start_time, end_time, step_time = tonumber(m[1]), tonumber(m[2]), tonumber(m[3])
        if start_time <= case.day_of_week and case.day_of_week <= end_time and math.fmod(case.day_of_week - start_time, step_time) == 0 then
            return true
        end
    else
        -- TODO
    end
    return false
end


local function match_year(pattern, case)
    if pattern.year == '' or pattern.year == '*' or pattern.year == '?' then
        return true
    elseif string.match(pattern.year, '^[0-9]+$') then
        if tonumber(pattern.year) == case.year then
            return true
        end
    elseif string.match(pattern.year, '^([0-9]+),([0-9]+)[^/]*$') then
        local pattern_years = split_string(pattern.year, ',')
        for i_pattern_year, v_pattern_year in ipairs(pattern_years) do
            if tonumber(v_pattern_year) == case.year then
                return true
            end
        end
    elseif string.match(pattern.year, '^([0-9]+)%-([0-9]+)$') then
        local pattern_years = split_string(pattern.year, '-')
        if tonumber(pattern_years[1]) <= case.year and case.year <= tonumber(pattern_years[2]) then
            return true
        end
    elseif string.match(pattern.year, '^([0-9]+)%-([0-9]+)/([0-9]+)$') then
        local m = {}
        for i in pattern.year:gmatch('[0-9]+') do
            table.insert(m, i)
        end
        local start_time, end_time, step_time = tonumber(m[1]), tonumber(m[2]), tonumber(m[3])
        if start_time <= case.year and case.year <= end_time and math.fmod(case.year - start_time, step_time) == 0 then
            return true
        end
    else
        -- TODO
    end
    return false
end


local function match_hour_minute_second(pattern, case)
    if pattern.hour_minute_second == '' or pattern.hour_minute_second == '*' or pattern.hour_minute_second == '?' then
        return true
    end
    local current_time = case.hour*3600 + case.minute*60 + case.second
    for i_pattern_hour_minute_second, v_pattern_hour_minute_second in ipairs(pattern.hour_minute_second) do
        if string.match(v_pattern_hour_minute_second, '^[012][0-9]:[0-5][0-9]:[0-5][0-9]%-[012][0-9]:[0-5][0-9]:[0-5][0-9]$') then
            local m = {}
            for i in v_pattern_hour_minute_second:gmatch('[0-9]+') do
                table.insert(m, tonumber(i))
            end
            local start_time, end_time = m[1]*3600 + m[2]*60 + m[3], m[4]*3600 + m[5]*60 + m[6]
            if start_time <= current_time and current_time <= end_time then
                return true
            end
        end
    end
    return false
end


local function match_day_of_trade(pattern, case)
    if pattern.day_of_trade == '' or pattern.day_of_trade == '*' or pattern.day_of_trade == '?' then
        return true
    elseif pattern.day_of_trade == case.day_of_trade then
        return true
    end
    return false
end


function match_std(pattern, case)
    local pattern = format_pattern(pattern)
    if not patterns or not case then
        return false
    end
    if match_second(pattern, case)
            and match_minute(pattern, case)
            and match_hour(pattern, case)
            and match_hour_minute_second(pattern, case)
            and match_day_of_month(pattern, case)
            and match_month(pattern, case)
            and match_day_of_week(pattern, case)
            and match_year(pattern, case)
            and match_day_of_trade(pattern, case)
        return true
    end
    return false
end


-- patterns = {
--     '* * * * *',
--     '* * * * * *',
--     '* * * * * * *',
--     {
--         second       = '*',
--         minute       = '*',
--         hour         = '*',
--         day_of_month = '*',
--         month        = '*',
--         day_of_week  = '*',
--         year         = '*',
--     },
--     {
--         hour_minute_second = { '00:00:00-00:00:00', '00:00:00-00:00:00', ... },
--         day_of_trade = '*' or '0' or '1',
--     },
--     ...
-- }
function match_ext(patterns, case)
    local case = format_case(case)
    for i_pattern, v_pattern in ipairs(patterns) do
        if match_std(v_pattern, case) then
            return true
        end
    end
    return false
end
