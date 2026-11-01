# 9. Launch hero kits
Twenty-four launch characters across eleven of the twelve role families (Archivist has no launch hero). Each has four abilities: three basic and one ultimate. Ultimates unlock at 6, 11 and 16.

Re-theme of the former launch kits onto the character set (bota/ROSTER.md). Slot in brackets = character number. Slot mapping follows the section 24 number, so it is GUESS. Every renamed ability and hero name is GUESS (theme only). Archetypes kept from the former kit (GUESS: each former archetype maps to a role family in plan/15).

Emergent rewrite (GUESS): each effect carries its character's gag (a visible trait from the character prompt). Ability IDs, slot order, the four-ability count, effect kinds and the tier numbers below are kept. Any number that moved is GUESS inline (decision 42). Every cross-hero hook is GUESS and lives only in Emergent hooks, at most one per row (a hero may be named as the partner in several rows). No new engine kinds or ability slots; ideas that need one are in Requests.

### Ability value tiers

Every ability uses one of these tiers. Every number here is UNVERIFIED until a playable build exists. Each hero's abilities are sized to them, with the role-family talent sets in section 21 added on top.

| Ability type | Level 1 | Level 2 | Level 3 | Level 4 | Cooldown (L1 to L4) | Sigma (L1 to L4) |
| --- | --- | --- | --- | --- | --- | --- |
| Ability 1, damage | 80 | 160 | 240 | 320 | 10, 9, 8, 7 s | 60, 70, 80, 90 |
| Ability 2, control or utility | 2.0 s | 2.5 s | 3.0 s | 3.5 s | 12, 11, 10, 9 s | 70, 80, 90, 100 |
| Ability 3, aura or passive | 300 radius | 350 radius | 400 radius | 450 radius | 14, 12, 10, 8 s | 0 (passive) or 50 |
| Ultimate (unlocks at 6, 11, 16) | 250 damage | 400 damage | 550 damage | n/a (max 3) | 100, 85, 70 s | 150, 200, 250 |

Notes:

- Stun and root durations scale with the ability 2 table. Status resistance (section 21) reduces them.
- Damage numbers are base values. Attribute scaling and item bonuses are added on top.
- Hooks name the other hero and the ability they touch. A hook that needs a counter read across heroes uses an existing unit counter from Lua (GUESS).

| Hero | Archetype | Ability 1 | Ability 2 | Ability 3 | Ultimate |
| --- | --- | --- | --- | --- | --- |
| Grey [077] | Drifter | Beam Quote: three-hit tractor-beam burst; each hit spends an Abduction Count stack for +10% damage (GUESS) | Abduction Count: collects a specimen stack when a nearby enemy dies, cap 5 (GUESS); an allied kill adds one too (GUESS) | Orb Vibes Aura: the levitating orb hums, cutting nearby enemy armor (GUESS) | Probe Ticker: lines of damage that probe the target; each line that kills adds an Abduction Count stack (GUESS) |
| Spudgunner [084] | Drifter | Pipe Spud: a spud fired from the pipe bursts into an area that damages and slows (GUESS); slowed enemies take +Pressure Gauge Reply damage (GUESS) | Pressure Gauge Reply: the gauge charges the next attack for bonus damage, doubled if the target stands in Pipe Spud (GUESS) | Ear Muff Span: extra attack range; the ear muffs block the noise, so nearby enemies do not wake from attacks (GUESS) | Long Shot Spud: long-range spud strike; a kill refunds half its cooldown to Pipe Spud (GUESS) |
| Tinfoil [073] | Drifter | Foil Mention: strikes from behind while unseen; the hat has spotted a government agent, bonus damage vs heroes (GUESS) | Foil Cloud: a crinkling foil cloud blinds enemies by glare (GUESS) | Coat Hanger Open: blinks to a target with the copper wire coat hanger and attacks; blink stops at walls (GUESS) | Crumple Ghost: invisible strike sequence; each strike drops a crumpled foil ball that revives a nearby ally once (GUESS) |
| Boomer [010] | Heckler | Pull Cord Hurl: yanks the weedwhacker cord and tosses it for a ranged slow (GUESS) | Ok Boomer Strike: next attack, with a dismissive wave, deals bonus damage (GUESS) | Cobalt Fade: blue-mirror sunglasses make him briefly invisible while moving; attacking flashes them and breaks the invisibility (GUESS) | Tracked Lawn: reveals an enemy; every hit leaves a grass stain that pays gold (GUESS) |
| Disaster [036] | Firebrand | Smirk Read: a devilish sideways smirk at the target freezes it in place (GUESS) | Fire Fade: fades into the fire glow, briefly invulnerable (GUESS) | Fire Wall of Text: a wall of burning letters blocks a path (GUESS) | Smolder Drop: delayed area damage; the house burns while she smirks at the viewer (GUESS) |
| Tricky [047] | Bulwark | Stop Sign Citation: hops and slams the octagon for slow and damage (GUESS) | Hockey Correction: a hockey-mask check turns the target into a sheep (GUESS) | Curl Drain: frizzy neon-red curls soak sigma while channeling (GUESS) | Octagon Source: must cite a dead enemy as the source to cast (GUESS); the citation damages everything in the octagon (GUESS) |
| Gigachad [004] | Bulwark | Flex Rebuttal: flexing damages per attack and drains sigma (GUESS) | Chiseled Step: short teleport in one unbroken stride (GUESS) | Monolith Block: a carved monolith blocks spell damage (GUESS) | Carved Gap Lot: damage scales with missing sigma, the empty marble gap (GUESS) |
| Noscope [039] | Stalker | Hitmarker Spin: spins and damages nearby enemies; each hit flashes the green crosshair hitmarker over the target (GUESS) | Sponsor Patch Heal: heals allies in radius; a healed ally also gets Noscope's Lucky Scope crit chance (GUESS) | Lucky Scope: the lens flare gives a chance to critically strike; a crit pays a sponsor bonus (GUESS) | Bolt Action Chain: rapid bolt-action strikes that jump between enemies (GUESS) |
| Viking [019] | Herald | Mead Bash: area damage and slow; the slow lasts while enemies stand in Water Bottle Regen's aura (GUESS) | Hammer Hold: the silver hammer pendant roots and damages over time (GUESS) | Water Bottle Regen: sigma regen for allies, sipped from a half-full bottle (GUESS) | Ragnarok March: area nuke around the hero; each rhythmic march step stomps the ground (GUESS) |
| Hank [046] | Tether | Machete Scroll: line of damage from a twin-machete swing (GUESS) | Lens Flash: crimson lenses flash for a delayed stun in an area (GUESS) | Machete Meter: attack speed and movement stacks; stacks are spent on Machete Clip (same hero, GUESS) | Machete Clip: single-target burst with the twin machetes; a kill resets Machete Meter (GUESS) |
| Boxxy [021] | Tether | Eyeliner Bleed: damage over time as the eyeliner runs; bleeding targets take the Emo Vibes armor cut (same hero, GUESS) | Sweater Slip: the oversized sweater slips off one shoulder to protect an ally from death briefly (GUESS) | Open Palm Bounce: animated open-palm gestures bounce to nearby units (GUESS) | Emo Vibes: reduces enemy armor; the cut doubles on targets already bleeding from Eyeliner Bleed (GUESS) |
| Waffle [062] | Bulwark | Pillbox Apology: the pillbox cap heals allies and damages enemies in a sorry-not-sorry burst (GUESS) | Tray Dismiss: immunity to selected debuffs; the tray knocks them off (GUESS) | Buckler Pin: the food tray is held as a buckler, damaging enemies in an area (GUESS) | Diner Likes: briefly invulnerable allies, a regular's tip for the table (GUESS) |
| Frogger [092] | Showboat | Flying Cap Warning: ear flaps flap to slow and damage (GUESS) | Handlebar Appeal: damage reduction on cooldown; the imaginary handlebars block hits (GUESS) | Frog Strike: mid-air crouching leap lands for area damage (GUESS) | Helmet Lockdown: white goggles lock on for a delayed area stun (GUESS) |
| Airhorn [088] | Heckler | Airhorn Blast: the brass canisters blast a stun and damage (GUESS) | Canister Remove: each attack empties a canister in a cleave (GUESS) | Track Jacket Notice: sponsor-stripe armor and speed for allies (GUESS) | Escalating Blare: damage increase; each stun Airhorn Blast applies adds to the blare (GUESS) |
| Helios [065] | Phantom | Marble Dagger: a marble dagger thrown from the floating bust slows and damages (GUESS) | Pedestal Rephrase: the bust floats to a target and teleports onto its pedestal (GUESS) | Mirror Shade Mode: mirrored sunglasses give evasion and stealth (GUESS) | Sun Lot: chance for critical damage in a neon-sun flash (GUESS) |
| Starwarskid [053] | Tether | Golf Pole Root: the hollow golf-ball pole roots an area (GUESS) | Mid-Spin Clone: a furrowed-brow clone; he teleports to it (GUESS) | Furrowed Puppet: a furrowed-brow puppet damages and slows (GUESS) | Alt Spin Squad: clones fight on their own, spinning in with the same focus (GUESS) |
| Chudjak [028] | Bulwark | Manifesto Slam: the rolled manifesto clubs a line of damage and stun (GUESS) | Olive Totem: the olive surplus jacket empowers attacks (GUESS) | Buzzcut Follow: a stun and damage around the hero with a severe scowl (GUESS) | Surplus Echo: surplus rage scales damage with nearby enemies (GUESS) |
| Wojak [005] | Recluse | Sigh at Clouds: a wistful sigh taunts enemies in range (GUESS) | Hollow Stare: downcast hollow eyes slow and damage over time (GUESS) | Sad Clapback: a wounded sigh returns damage when attacked (GUESS) | Sorrowful Cancel: instant kill below 25% health (GUESS, threshold UNVERIFIED) |
| Ghillie [089] | Stalker | Burlap Warning: burlap strips scatter as area traps with damage (GUESS) | Twine Lock: camouflage twine holds and reveals enemies (GUESS) | Corn Stalk Jump: leaping strike with damage; a jump over a trap triggers it early (GUESS) | Scoped Temp Ban: remote detonation through the scope disables (GUESS) |
| Fuckyea [069] | Showboat | Noir Hook: black sunglasses hook and pull a target (GUESS) | Jacket Stale: damage over time and slow in an area (GUESS) | Smug Stacks: gains strength with each kill, smugly (GUESS) | Pocket Edit: hands stay in pockets while a channel damages and pulls (GUESS) |
| Forever [068] | Recluse | Tear Clip: a single tear projectile; a slowed target keeps the tear stuck (GUESS) | Lumpy Wail: a weeping wail damages around the hero (GUESS) | Crawl Ghost: brief evasion while crawling low (GUESS) | Eternal Loop: the weeping stun repeats until the clip ends, forever (GUESS) |
| Scammer [110] | Tether | Landline Teaser: a tangled phone cord line deals damage and burn (GUESS) | Bluetooth Bait: a blinking lifesteal aura for allies in range (GUESS) | Sales Pitch Bait: critical strikes from a rapid sales pitch (GUESS) | Cord Coil Arc: the tangled cord pulls him back on death (GUESS) |
| Prepper [057] | Bulwark | Gas Mask Air: a gas mask roots an area (GUESS) | Blast Door Leave: the blast door slams into place and carries him to an ally (GUESS) | Storm Shelter: summons treants wrapped in duct tape (GUESS) | Hazmat Breach: a damage breach through the hazmat suit (GUESS) |
| Lifehack [096] | Engine | Glue Gun Camouflage: invisibility in trees; the hot glue sticks him there (GUESS) | Zip Tie Market: drains enemy health with neon zip ties (GUESS) | Duct Tape Shield: shields an ally with rainbow duct tape (GUESS) | Zip Tie Network: roots and damages nearby enemies in a manic web of zip ties (GUESS) |

Notes:

- Marble Dagger (Helios [065], Ability 1) keeps the dagger role. It throws a dagger.
- Mirror Shade Mode (Helios [065], Ability 3) is the invisibility effect. The item Anon Mask (section 11) is separate.
- Talent trees are in section 21.

### Emergent hooks

Heroes with no hook: Forever [068], Lifehack [096].

- Grey [077] with Smugjak [029]: Orb Vibes and Smug Citation armor cuts stack (GUESS).
- Spudgunner [084] with Greg [034]: Polo Flak victims stay inside the Ear Muff Span attack range (GUESS).
- Tinfoil [073] with Glitch [076]: Foil Mention exposes the target to Chromatic Hold (GUESS).
- Boomer [010] with Wojak [005]: Pull Cord Hurl slowed targets draw Hollow Stare (GUESS).
- Disaster [036] with Attached [037]: Smile Shift relocates the Smolder Drop victim (GUESS).
- Tricky [047] with Hypebeast [060]: sheep targets stay open to Box Spike (GUESS).
- Gigachad [004] with Yao [032]: Chiseled Step can land on Tracksuit Hole points (GUESS).
- Noscope [039] with Scammer [110]: Hitmarker tags are the Sales Pitch Bait targets (GUESS).
- Viking [019] with Prepper [057]: Blast Door Leave walls pin Hammer Hold targets (GUESS).
- Hank [046] with Jack [043]: a Machete Clip kill resets Jack's Tar Pulse cooldown (GUESS).
- Boxxy [021] with Gopnik [050]: Sweater Slip protected allies draw Newsboy Chat boosts (GUESS).
- Waffle [062] with Saxguy [023]: Tray Dismiss clears Sax Solo Lock silence (GUESS).
- Frogger [092] with Chudjak [028]: Frog Strike landings leave Manifesto Slam stun points (GUESS).
- Airhorn [088] with Chudjak [028]: Airhorn Blast knocks Buzzcut Follow victims (GUESS).
- Helios [065] with Oiler [093]: Marble Dagger pins the Lavender Boomerang return path (GUESS).
- Starwarskid [053] with Gigaunit [101]: Mid-Spin Clone position is read by Layer Swap (GUESS).
- Ghillie [089] with Droner [090]: Drone Pursuit reveals Burlap Warning traps (GUESS).
- Fuckyea [069] with Challenge [070]: Folded Arms Cloak refuses Pocket Edit pulls (GUESS).

### Requests

- A cross-hero unit-counter read that does not need Lua per hook (GUESS): several hooks above read another hero's stack; a shared stack channel would make them plain data.
- An armor-cut stack rule that caps combined armor cuts (GUESS): Orb Vibes and Smug Citation stack to a combined armour cut of 4 (GUESS, no 6.88g source); no further limit in the current kit.
