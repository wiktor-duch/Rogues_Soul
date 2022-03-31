class Statistics():
    ''' This class handles statistics updating and printing. '''
    def __init__(self, max_lvl:int = 3) -> None:
        self.max_lvl = max_lvl
        ## General
        self.valid_actions = 0
        self.invalid_actions = 0
        self.time_elapsed = 0
        self.levels_completed = 0
        self.gym_reward = 0
        ## Map discovering
        self.rooms_lvl_1 = 0
        self.rooms_lvl_2 = 0
        self.rooms_lvl_3 = 0
        self.tot_rooms = 0
        self.rooms_visited_lvl_1 = 0
        self.rooms_visited_lvl_2 = 0
        self.rooms_visited_lvl_3 = 0
        self.rooms_visted = 0
        self.fov_updates = 0
        ## Player Final Stats
        self.hp = 0
        self.defense = 0
        self.power = 0
        self.souls = 0
        ## Equipment
        self.eqp_available = 0
        self.swords_collected = 0
        self.shields_collected = 0
        self.armours_collected = 0
        self.eqp_collected_lvl_1 = 0
        self.eqp_collected_lvl_2 = 0
        self.eqp_collected_lvl_3 = 0
        self.tot_eqp_collected = 0
        ## Enemies
        self.num_enemies = 0
        self.enemies_killed = 0
        self.enemies_lvl_1 = 0
        self.enemies_lvl_2 = 0
        self.enemies_lvl_3 = 0
        self.enemies_killed_lvl_1 = 0
        self.enemies_killed_lvl_2 = 0
        self.enemies_killed_lvl_3 = 0
        ## Items
        # Chests
        self.opened_chests = 0
        self.num_chests = 0
        self.opened_traps = 0
        self.opened_rewards = 0
        # Health Potions
        self.potions_available = 0
        self.potions_used = 0
        self.hp_lost = 0
        self.hp_gained = 0
        # Souls
        self.souls_collected = 0
        self.souls_collected_lvl_1 = 0
        self.souls_collected_lvl_2 = 0
        self.souls_collected_lvl_3 = 0
        self.souls_available = 0
        self.souls_available_lvl_1 = 0
        self.souls_available_lvl_2 = 0
        self.souls_available_lvl_3 = 0
    
    def get_gym_reward(self) -> int:
        # Returns the approximation of env reward function value.
        reward = 0
        if self.levels_completed != self.max_lvl:
            reward -= 100 # Dying at some level
        reward += self.fov_updates # New tiles discovered
        reward += self.levels_completed * 100 # Levels completed
        reward += self.souls # Soul items and chests Souls collected
        return reward

    def display(self) -> None:
        ''' Prints all the statistics. '''
        
        hline = '\n|---------------------------------------|'
        
        # Header
        header = (
            hline
            + '\n|\t\tSTATISTICS\t\t|'
            + hline
        )
        print(header)
        # General
        general = '| General:'
        for _ in range(40-len(general)):
            general += ' '
        general += '|'
        time = '\n|\tTime elapsed (s): ' + str(self.time_elapsed)
        for _ in range(35-len(time)):
            time += ' '
        general += time + '|'
        vact = '\n|\tNum. of valid actions: ' + str(self.valid_actions)
        for _ in range(35-len(vact)):
            vact += ' '
        general += vact + '|'
        invact = '\n|\tNum. of invalid actions: ' + str(self.invalid_actions)
        for _ in range(35-len(invact)):
            invact += ' '
        general += invact + '|'
        lvl = '\n|\tLevels completed: ' + str(self.levels_completed)
        for _ in range(35-len(lvl)):
            lvl += ' '
        general += lvl + '|'
        self.gym_reward = self.get_gym_reward()
        gym = '\n|\tOpenAI Gym reward: ' + str(self.gym_reward)
        for _ in range(35-len(gym)):
            gym += ' '
        general += gym + '|'
        general += hline
        print(general)
        # Map
        map = '| Map:'
        for _ in range(40-len(map)):
            map += ' '
        map += '|'

        rms = '\n|\tRooms (visited/all)'
        for _ in range(35-len(rms)):
            rms += ' '
        map += rms + '|'
        rms1 = '\n|\t   Level 1: (' + str(self.rooms_visited_lvl_1) + '/' + str(self.rooms_lvl_1) + ')'
        for _ in range(35-len(rms1)):
            rms1 += ' '
        map += rms1 + '|'
        if self.max_lvl >= 2:
            rms2 = '\n|\t   Level 2: (' + str(self.rooms_visited_lvl_2) + '/' + str(self.rooms_lvl_2) + ')'
            for _ in range(35-len(rms2)):
                rms2 += ' '
            map += rms2 + '|'
        if self.max_lvl >= 3:
            rms3 = '\n|\t   Level 3: ' + str(self.rooms_visited_lvl_3) + '/' + str(self.rooms_lvl_3) + ')'
            for _ in range(35-len(rms3)):
                rms3 += ' '
            map += rms3 + '|'
        if self.max_lvl >= 2:
            rmst = '\n|\t   Total: (' + str(self.rooms_visted) + '/' + str(self.tot_rooms) + ')'
            for _ in range(35-len(rmst)):
                rmst += ' '
            map += rmst + '|'
        fov = '\n|\tFOV updates: ' + str(self.fov_updates)
        for _ in range(35-len(fov)):
            fov += ' '
        map += fov + '|'
        map += hline
        print(map)
        # Player
        plr = '| Player:'
        for _ in range(40-len(plr)):
            plr += ' '
        plr += '|'
        mhp = '\n|\tMax HP: ' + str(self.hp)
        for _ in range(35-len(mhp)):
            mhp += ' '
        plr += mhp + '|'
        dfs = '\n|\tDefense: ' + str(self.defense)
        for _ in range(35-len(dfs)):
            dfs += ' '
        plr += dfs + '|'
        pow = '\n|\tPower: ' + str(self.power)
        for _ in range(35-len(pow)):
            pow += ' '
        plr += pow + '|'
        sls = '\n|\tSouls: ' + str(self.souls)
        for _ in range(35-len(sls)):
            sls += ' '
        plr += sls + '|'
        plr += hline
        print(plr)
        # Equipment
        eqp = '| Equipment:'
        for _ in range(40-len(eqp)):
            eqp += ' '
        eqp += '|'
        swd = '\n|\tSwords collected: ' + str(self.swords_collected)
        for _ in range(35-len(swd)):
            swd += ' '
        eqp += swd + '|'
        shd = '\n|\tShields collected: ' + str(self.shields_collected)
        for _ in range(35-len(shd)):
            shd += ' '
        eqp += shd + '|'
        arm = '\n|\tArmours collected: ' + str(self.armours_collected)
        for _ in range(35-len(arm)):
            arm += ' '
        eqp += arm + '|'
        eqp_tot = '\n|\tEquipment available: ' + str(self.eqp_available)
        for _ in range(35-len(eqp_tot)):
            eqp_tot += ' '
        eqp += eqp_tot + '|'
        clct = '\n|\tEquipment collected:'
        for _ in range(35-len(clct)):
            clct += ' '
        eqp += clct + '|'
        clct_1 = '\n|\t   Level 1: ' + str(self.eqp_collected_lvl_1)
        for _ in range(35-len(clct_1)):
            clct_1 += ' '
        eqp += clct_1 + '|'
        if self.max_lvl >= 2:
            clct_2 = '\n|\t   Level 2: ' + str(self.rooms_visited_lvl_2)
            for _ in range(35-len(clct_2)):
                clct_2 += ' '
            eqp += clct_2 + '|'
        if self.max_lvl >= 3:
            clct_3 = '\n|\t   Level 3: ' + str(self.eqp_collected_lvl_3)
            for _ in range(35-len(clct_3)):
                clct_3 += ' '
            eqp += clct_3 + '|'
        if self.max_lvl >= 2:
            clct_t = '\n|\t   Total: ' + str(self.tot_eqp_collected)
            for _ in range(35-len(clct_t)):
                clct_t += ' '
            eqp += clct_t + '|'
        eqp += hline
        print(eqp)
        # Enemies 
        enm = '| Enemies:(killed/all)'
        for _ in range(40-len(enm)):
            enm += ' '
        enm += '|'
        enm_1 = '\n|\tLevel 1: (' + str(self.enemies_killed_lvl_1) + '/' + str(self.enemies_lvl_1) + ')'
        for _ in range(35-len(enm_1)):
            enm_1 += ' '
        enm += enm_1 + '|'
        if self.max_lvl >= 2:
            enm_2 = '\n|\tLevel 2: (' + str(self.enemies_killed_lvl_2) + '/' + str(self.enemies_lvl_2) + ')'
            for _ in range(35-len(enm_2)):
                enm_2 += ' '
            enm += enm_2 + '|'
        if self.max_lvl >= 3:
            enm_3 = '\n|\tLevel 3: (' + str(self.enemies_killed_lvl_3) + '/' + str(self.enemies_lvl_3) + ')'
            for _ in range(35-len(enm_3)):
                enm_3 += ' '
            enm += enm_3 + '|'
        if self.max_lvl >= 2:
            enm_t = '\n|\tTotal: (' + str(self.enemies_killed) + '/' + str(self.num_enemies) + ')'
            for _ in range(35-len(enm_t)):
                enm_t += ' '
            enm += enm_t + '|'
        enm += hline
        print(enm)
        # Items
        itm = '| Items:'
        for _ in range(40-len(itm)):
            itm += ' '
        itm += '|'
        cst = '\n|\tChests:'
        for _ in range(35-len(cst)):
            cst += ' '
        itm += cst + '|'
        cst = '\n|\t   Contained reward: ' + str(self.opened_rewards)
        for _ in range(35-len(cst)):
            cst += ' '
        itm += cst + '|'
        cst = '\n|\t   Contained trap: ' + str(self.opened_traps)
        for _ in range(35-len(cst)):
            cst += ' '
        itm += cst + '|'
        cst = '\n|\t   Opened: ' + str(self.opened_chests)
        for _ in range(35-len(cst)):
            cst += ' '
        itm += cst + '|'
        cst = '\n|\t   Available: ' + str(self.num_chests)
        for _ in range(35-len(cst)):
            cst += ' '
        itm += cst + '|'
        hpp = '\n|\tHealth Potions:'
        for _ in range(35-len(hpp)):
            hpp += ' '
        itm += hpp + '|'
        hpp = '\n|\t   Consumed:' + str(self.potions_used)
        for _ in range(35-len(hpp)):
            hpp += ' '
        itm += hpp + '|'
        hpp = '\n|\t   Available: ' + str(self.potions_available)
        for _ in range(35-len(hpp)):
            hpp += ' '
        itm += hpp + '|'
        hpp = '\n|\t   HP gained: ' + str(self.hp_gained)
        for _ in range(35-len(hpp)):
            hpp += ' '
        itm += hpp + '|'
        hpp = '\n|\t   HP lost :' + str(self.hp_lost)
        for _ in range(35-len(hpp)):
            hpp += ' '
        itm += hpp + '|'
        
        sls = '\n|\tSouls: (collected/all)'
        for _ in range(35-len(sls)):
            sls += ' '
        itm += sls + '|'
        sls = '\n|\t   Level 1: (' + str(self.souls_collected_lvl_1) + '/' + str(self.souls_available_lvl_1) + ')'
        for _ in range(35-len(sls)):
            sls += ' '
        itm += sls + '|'
        if self.max_lvl >= 2:
            sls = '\n|\t   Level 2: (' + str(self.souls_collected_lvl_2) + '/' + str(self.souls_available_lvl_2) + ')'
            for _ in range(35-len(sls)):
                sls += ' '
            itm += sls + '|'
        if self.max_lvl >= 3:
            sls = '\n|\t   Level 3: (' + str(self.souls_collected_lvl_3) + '/' + str(self.souls_available_lvl_3) + ')'
            for _ in range(35-len(sls)):
                sls += ' '
            itm += sls + '|'
        if self.max_lvl >= 2:
            sls = '\n|\t   Total: (' + str(self.souls_collected) + '/' + str(self.souls_available) + ')'
            for _ in range(35-len(sls)):
                sls += ' '
            itm += sls + '|'
        itm += hline
        print(itm)