# 22. Art direction

Visual direction for the 59 heroes (kept characters from characters). Each row takes its distinct prop from the character prompt. Role families come from section 15. Shape, value and colour rules come from plan/17.

## Rules used in every table

- **Body codes.** P1 taller (+10% height). P2 broader (+15% width). P3 compact (-10% height). P4 longer (+15% length). P5 short legs (-20% leg length). P6 big head (+20% head size). All percentages are design targets, UNVERIFIED.
- **Value groups.** Written as body / head / prop, using L (light), M (mid) and D (dark). Head and prop each differ from body by the 30% luminance delta in section 17. Mapping: L about 85%, M about 55%, D about 25% luminance, all UNVERIFIED.
- **Head and prop default.** Body L gives head D, prop M. Body M gives head L, prop D. Body D gives head L, prop M. Set by rule, not by the prompt.
- **Primary value group** is the body value.
- **Sibling rule.** Within a role family, take the hero's 0-based index k in roster order. Body code is P(k mod 6 + 1). Body value is L, M, D for floor(k/6) = 0, 1, 2. Every prop in a role family is unique, except for a hero with no held prop (plan/20 decision 25). Two siblings that both carry a prop differ in prop silhouette and in at least one of body code or body value. A hero with no held prop differs from each sibling in both body code and body value, which meets the two-of-three rule in section 15.
- **Accent shifts** are named steps from the role family accent (section 15). No hex is set here.
- **Color guards.** Hero trim stays off the plan/17 colour table; use a desaturated violet outside the Clout and LIVE violets. Firebrand ember and Leash rose shift off red. Herald cyan shifts off heal green. Phantom lavender stays low in saturation so it does not read as Showboat violet.

## 1. Hero table (59)

| # | Hero | Role | Distinct prop | Accent shift | Value groups (body / head / prop) |
| --- | --- | --- | --- | --- | --- |
| 001 | Neckbeard (P1) | Heckler | Round wire-rim glasses (worn; no held prop) | Mustard, dingy | L / D / M |
| 002 | Chonky Hop (P1) | Bulwark | Suspenders (worn; no held prop) | Grey, soft | L / D / M |
| 003 | Chad (P1) | Showboat | Hands-on-hips pose (no held prop) | Gold, emerald | L / D / M |
| 004 | Gigachad (P2) | Bulwark | Swim briefs (worn; no held prop) | Grey, monochrome | L / D / M |
| 005 | Wojak (P1) | Recluse | Slumped posture (no held prop) | Moss, faded | L / D / M |
| 008 | Bloomer (P2) | Herald | Pastel windbreaker zip (worn; no held prop) | Soft cyan, pastel yellow | L / D / M |
| 009 | Tradwife (P3) | Herald | Braided brioche loaf in oven mitts | Sky blue, cream | L / D / M |
| 010 | Boomer (P2) | Heckler | Pull-cord gas weedwhacker at the hip | Mustard, khaki | L / D / M |
| 011 | Coomer (P1) | Firebrand | Massive right arm (no held prop) | Ember, bloodshot | L / D / M |
| 012 | Gondola (P2) | Recluse | Two boots as the base (no held prop) | Moss, clay brown | L / D / M |
| 013 | Spurdo (P2) | Firebrand | Dented aluminum baseball bat | Ember, olive | L / D / M |
| 014 | Karen (P3) | Heckler | Endless accordion-folded receipt | Mustard, pastel pink | L / D / M |
| 015 | Trevor (P3) | Firebrand | Two shattered drywall slabs held as knuckles | Ember, white-hot | L / D / M |
| 016 | Howard (P1) | Archivist | White ceramic mug, WORLD'S BEST | Sepia, pale | L / D / M |
| 017 | Sanic (P1) | Stalker | Running lean (no held prop) | Slate, electric blue | L / D / M |
| 018 | Lankdad (P1) | Phantom | Black tendrils from the upper spine | Lavender, black | L / D / M |
| 019 | Viking (P4) | Herald | Half-full clear water bottle | Soft cyan, steel | L / D / M |
| 021 | Smudge (P1) | Leash | Open-palm gestures (no held prop) | Rose, grey | L / D / M |
| 025 | Finger Dan (P4) | Heckler | Pointing arm (no held prop) | Mustard, bronze | L / D / M |
| 027 | Willie (P1) | Engine | Free-floating brass ship bell | Cold teal, black and white | L / D / M |
| 028 | Chudjak (P3) | Bulwark | Rolled brown paper manifesto | Grey, olive | L / D / M |
| 029 | Smugjak (P4) | Showboat | Hands clasped behind back (no held prop) | Peach, burgundy | L / D / M |
| 030 | Rageguy (P5) | Firebrand | Raised fists (no held prop) | Ember, stark white | L / D / M |
| 031 | Cereal (P5) | Heckler | Oversized steel tablespoon | Mustard, white | L / D / M |
| 039 | Noscope (P2) | Stalker | Bolt-action precision rifle | Slate, sponsor green | L / D / M |
| 040 | Dino (P4) | Bulwark | Tyrannosaur body (no held prop) | Grey, stark | L / D / M |
| 041 | Fuuuu (P4) | Recluse | Hands clutching temples (no held prop) | Moss, pale | L / D / M |
| 042 | Jeff (P3) | Stalker | Cast-iron frying pan held low | Slate, bleached white | L / D / M |
| 043 | Jack (P4) | Stalker | Polished steel surgical scalpel | Slate, royal blue | L / D / M |
| 044 | Salad (P4) | Drifter | Three silver spoons between knuckles | Night blue, olive | L / D / M |
| 047 | Tricky (P5) | Bulwark | Octagonal stop sign on an iron pipe | Grey, decay green | L / D / M |
| 049 | Ecce (P3) | Archivist | Wooden painter's palette with paint blobs | Sepia, burlap | L / D / M |
| 054 | Bot Bernard (P6) | Herald | Vintage chrome studio camera | Soft cyan, burgundy | L / D / M |
| 055 | Shoop (P6) | Drifter | Plasma sphere charging in the mouth | Night blue, bright cyan | L / D / M |
| 066 | Npc (P5) | Phantom | Arms hanging straight down (no held prop) | Lavender, slate | L / D / M |
| 067 | Derp (P6) | Recluse | Loosened crooked necktie (worn; no held prop) | Moss, white | L / D / M |
| 068 | Forever (P1) | Recluse | Hunched crawl, tear-stained tissue in hand | Moss, grey | M / L / D |
| 069 | Fuckyea (P2) | Showboat | Hands jammed in trouser pockets | Peach, jet black | M / L / D |
| 070 | Challenge (P5) | Leash | Folded arms across the chest | Rose, crisp white | L / D / M |
| 071 | Hipster (P2) | Herald | Glass teapot | Soft cyan, mustard | M / L / D |
| 076 | Glitch (P1) | Phantom | Offset chromatic duplicate layers (no held prop) | Lavender, neon | M / L / D |
| 077 | Grey (P4) | Drifter | Levitating metallic silver orb | Night blue, grey | M / L / D |
| 082 | Paintballer (P6) | Stalker | Electronic speedball marker with hopper | Slate, neon | L / D / M |
| 084 | Spudgunner (P5) | Drifter | Shoulder-mounted PVC pipe cannon | Night blue, buffalo tan | M / L / D |
| 088 | Airhorn (P3) | Heckler | Dual brass compressed-air horn canisters | Mustard, brass | M / L / D |
| 089 | Ghillie (P1) | Stalker | Scoped hunting rifle wrapped in twine | Slate, burlap | M / L / D |
| 097 | Carpool (P1) | Engine | Phone on a vent mount, wicker basket of candies | Cold teal, mint | M / L / D |
| 098 | Widemouth (P4) | Showboat | Huge smile, a cardboard hand fan held at the chest | Peach, white | M / L / D |
| 102 | Disheartened (P4) | Recluse | Crumpled receipt, half out of a pocket | Moss, charcoal | M / L / D |
| 103 | Pointing (P4) | Heckler | Yellow yardstick held across the chest | Mustard, blue | M / L / D |
| 106 | Gothgirl (P5) | Recluse | Black lace fan | Moss, black | M / L / D |
