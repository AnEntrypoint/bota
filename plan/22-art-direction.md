# 22. Art direction

Visual direction for the 112 heroes (roster 001 to 112, characters from characters). Each row takes its distinct prop from the character prompt. Role families come from section 15. Shape, value and colour rules come from plan/17.

## Rules used in every table

- **Body codes.** P1 taller (+10% height). P2 broader (+15% width). P3 compact (-10% height). P4 longer (+15% length). P5 short legs (-20% leg length). P6 big head (+20% head size). All percentages are design targets, UNVERIFIED.
- **Value groups.** Written as body / head / prop, using L (light), M (mid) and D (dark). Head and prop each differ from body by the 30% luminance delta in section 17. Mapping: L about 85%, M about 55%, D about 25% luminance, all UNVERIFIED.
- **Head and prop default.** Body L gives head D, prop M. Body M gives head L, prop D. Body D gives head L, prop M. Set by rule, not by the prompt.
- **Primary value group** is the body value.
- **Sibling rule.** Within a role family, take the hero's 0-based index k in roster order. Body code is P(k mod 6 + 1). Body value is L, M, D for floor(k/6) = 0, 1, 2. Every prop in a role family is unique, except for a hero with no held prop (plan/20 decision 25). Two siblings that both carry a prop differ in prop silhouette and in at least one of body code or body value. A hero with no held prop differs from each sibling in both body code and body value, which meets the two-of-three rule in section 15.
- **Accent shifts** are named steps from the role family accent (section 15). No hex is set here.
- **Color guards.** Keep #A35CFF and #6A1FD1 off hero trim; use a desaturated violet outside both. Keep red (damage only), #2E8BFF and #FF8A1F (team colors), and #3DDC97 (heal) off hero trim. Firebrand ember and Leash rose shift off red. Herald cyan shifts off heal green. Phantom lavender stays low in saturation so it does not read as Showboat violet.

## 1. Hero table (112)

| # | Hero | Role | Distinct prop | Accent shift | Value groups (body / head / prop) |
| --- | --- | --- | --- | --- | --- |
| 001 | Neckbeard (P1) | Heckler | Round wire-rim glasses (worn; no held prop) | Mustard, dingy | L / D / M |
| 002 | Chungus (P1) | Bulwark | Suspenders (worn; no held prop) | Grey, soft | L / D / M |
| 003 | Chad (P1) | Showboat | Hands-on-hips pose (no held prop) | Peach, emerald | L / D / M |
| 004 | Gigachad (P2) | Bulwark | Swim briefs (worn; no held prop) | Grey, monochrome | L / D / M |
| 005 | Wojak (P1) | Recluse | Slumped posture (no held prop) | Moss, faded | L / D / M |
| 006 | Soyjak (P1) | Herald | Gaping mouth (no held prop) | Soft cyan, yellow | L / D / M |
| 007 | Doomer (P1) | Drifter | Glowing cigarette with smoke plume | Night blue, smoky | L / D / M |
| 008 | Bloomer (P2) | Herald | Pastel windbreaker zip (worn; no held prop) | Soft cyan, pastel yellow | L / D / M |
| 009 | Tradwife (P3) | Herald | Braided brioche loaf in oven mitts | Sky blue, cream | L / D / M |
| 010 | Boomer (P2) | Heckler | Pull-cord gas weedwhacker at the hip | Mustard, khaki | L / D / M |
| 011 | Coomer (P1) | Firebrand | Massive right arm (no held prop) | Ember, bloodshot | L / D / M |
| 012 | Gondola (P2) | Recluse | Two boots as the base (no held prop) | Moss, clay brown | L / D / M |
| 013 | Spurdo (P2) | Firebrand | Dented aluminum baseball bat | Ember, olive | L / D / M |
| 014 | Karen (P3) | Heckler | Endless accordion-folded receipt | Mustard, pastel pink | L / D / M |
| 015 | Kyle (P3) | Firebrand | Two shattered drywall slabs held as knuckles | Ember, white-hot | L / D / M |
| 016 | Harold (P1) | Archivist | White ceramic mug, WORLD'S BEST | Sepia, pale | L / D / M |
| 017 | Sanic (P1) | Stalker | Running lean (no held prop) | Slate, electric blue | L / D / M |
| 018 | Slender (P1) | Phantom | Black tendrils from the upper spine | Lavender, black | L / D / M |
| 019 | Viking (P4) | Herald | Half-full clear water bottle | Soft cyan, steel | L / D / M |
| 020 | Leeroy (P4) | Firebrand | Broadsword held overhead | Ember, gold | L / D / M |
| 021 | Boxxy (P1) | Leash | Open-palm gestures (no held prop) | Rose, grey | L / D / M |
| 022 | Rickroll (P2) | Showboat | Vintage chrome broadcast mic on stand | Peach, ginger | L / D / M |
| 023 | Saxguy (P3) | Showboat | Polished brass alto saxophone | Peach, neon | L / D / M |
| 024 | Numa (P5) | Herald | Oversized grey studio headphones | Soft cyan, pale blue | L / D / M |
| 025 | Dodson (P4) | Heckler | Pointing arm (no held prop) | Mustard, bronze | L / D / M |
| 026 | Sweetbrown (P2) | Drifter | Red cherry pop held at chin height | Night blue, warm | L / D / M |
| 027 | Willie (P1) | Engine | Free-floating brass ship bell | Cold teal, black and white | L / D / M |
| 028 | Chudjak (P3) | Bulwark | Rolled brown paper manifesto | Grey, olive | L / D / M |
| 029 | Smugjak (P4) | Showboat | Hands clasped behind back (no held prop) | Peach, burgundy | L / D / M |
| 030 | Rageguy (P5) | Firebrand | Raised fists (no held prop) | Ember, stark white | L / D / M |
| 031 | Cereal (P5) | Heckler | Oversized steel tablespoon | Mustard, white | L / D / M |
| 032 | Yao (P6) | Heckler | Dismissive hand-wave (no held prop) | Mustard, warm | L / D / M |
| 033 | Steve (P3) | Drifter | Metallic flip stopwatch held forward | Night blue, brown | L / D / M |
| 034 | Greg (P3) | Recluse | Unlit rolled cigarette between lips | Moss, golden | L / D / M |
| 035 | Brian (P2) | Archivist | Metal wire braces (worn; no held prop) | Sepia, plaid | L / D / M |
| 036 | Disaster (P6) | Firebrand | Fire glow behind the silhouette (no held prop) | Ember, orange | L / D / M |
| 037 | Attached (P2) | Leash | Hands clasped under the chin (no held prop) | Rose, cool | L / D / M |
| 038 | Zyzz (P5) | Showboat | Aviator sunglasses on the chest | Peach, neon pink | L / D / M |
| 039 | Noscope (P2) | Stalker | Bolt-action precision rifle | Slate, sponsor green | L / D / M |
| 040 | Dino (P4) | Bulwark | Tyrannosaur body (no held prop) | Grey, stark | L / D / M |
| 041 | Fuuuu (P4) | Recluse | Hands clutching temples (no held prop) | Moss, pale | L / D / M |
| 042 | Jeff (P3) | Stalker | Steel kitchen butcher knife | Slate, bleached white | L / D / M |
| 043 | Jack (P4) | Stalker | Polished steel surgical scalpel | Slate, royal blue | L / D / M |
| 044 | Salad (P4) | Drifter | Three silver spoons between knuckles | Night blue, olive | L / D / M |
| 045 | Weegee (P2) | Phantom | Hypnotic stare (no held prop) | Lavender, emerald | L / D / M |
| 046 | Hank (P3) | Leash | Twin high-carbon machetes | Rose, charcoal | L / D / M |
| 047 | Tricky (P5) | Bulwark | Octagonal stop sign on an iron pipe | Grey, decay green | L / D / M |
| 048 | Peanut (P5) | Recluse | Spray-painted facial markings (no held prop) | Moss, concrete tan | L / D / M |
| 049 | Ecce (P3) | Archivist | Wooden painter's palette with paint blobs | Sepia, burlap | L / D / M |
| 050 | Gopnik (P1) | Firebrand | Steel crowbar across the knees | Ember, royal blue | M / L / D |
| 051 | Mallcop (P6) | Bulwark | Two-wheeled motorized scooter | Grey, navy | L / D / M |
| 052 | Vapebro (P5) | Drifter | Brass mechanical box-mod vape | Night blue, brass | L / D / M |
| 053 | Starwarskid (P4) | Leash | Hollow plastic golf-ball retriever pole | Rose, grey | L / D / M |
| 054 | Tay (P6) | Herald | Vintage chrome studio camera | Soft cyan, burgundy | L / D / M |
| 055 | Shoop (P6) | Drifter | Plasma sphere charging in the mouth | Night blue, bright cyan | L / D / M |
| 056 | Kazoo (P6) | Showboat | Glossy red plastic kazoo | Peach, apricot | L / D / M |
| 057 | Prepper (P1) | Bulwark | Steel storm-shelter blast door | Grey, olive | M / L / D |
| 058 | Trollhunter (P2) | Bulwark | Heavy wooden auction gavel | Grey, navy tie | M / L / D |
| 059 | Barista (P1) | Herald | Stainless portafilter handle | Soft cyan, denim | M / L / D |
| 060 | Hypebeast (P1) | Showboat | Stack of branded shoeboxes | Peach, sand | M / L / D |
| 061 | Florida (P2) | Firebrand | Two live alligators under the arms | Ember, neon yellow | M / L / D |
| 062 | Waffle (P3) | Bulwark | Heavy stainless food tray on one palm | Grey, pastel | M / L / D |
| 063 | Tpose (P3) | Phantom | Wireframe grid on the torso (no held prop) | Lavender, neon green | L / D / M |
| 064 | Zalgo (P1) | Drifter | Corrupted Unicode splinters (no held prop) | Night blue, black | M / L / D |
| 065 | Helios (P4) | Phantom | Floating marble bust and mirrored sunglasses | Lavender, pastel cyan | L / D / M |
| 066 | Npc (P5) | Phantom | Arms hanging straight down (no held prop) | Lavender, slate | L / D / M |
| 067 | Derp (P6) | Recluse | Loosened crooked necktie (worn; no held prop) | Moss, white | L / D / M |
| 068 | Forever (P1) | Recluse | Hunched crawl, tear-stained tissue in hand | Moss, grey | M / L / D |
| 069 | Fuckyea (P2) | Showboat | Hands jammed in trouser pockets | Peach, jet black | M / L / D |
| 070 | Challenge (P5) | Leash | Folded arms across the chest | Rose, crisp white | L / D / M |
| 071 | Hipster (P2) | Herald | Glass teapot | Soft cyan, mustard | M / L / D |
| 072 | Brony (P6) | Phantom | Staff topped with a glitter rainbow star | Lavender, pastel | L / D / M |
| 073 | Tinfoil (P2) | Drifter | Copper wire coat-hanger antenna as a wand | Night blue, silver | M / L / D |
| 074 | Flatearth (P4) | Archivist | Brass spirit level and glass dome | Sepia, map cream | L / D / M |
| 075 | Deepfried (P3) | Drifter | Lens-flare beams from the eye sockets (no held prop) | Night blue, saturated green | M / L / D |
| 076 | Glitch (P1) | Phantom | Offset chromatic duplicate layers (no held prop) | Lavender, neon | M / L / D |
| 077 | Grey (P4) | Drifter | Levitating metallic silver orb | Night blue, grey | M / L / D |
| 078 | Critic (P5) | Archivist | Antique 35mm film canister held overhead | Sepia, black | L / D / M |
| 079 | Crossfit (P2) | Engine | Knobby rubber tractor tire mid-roll | Cold teal, black | L / D / M |
| 080 | Acorn (P5) | Stalker | Two-handed combat pistol grip | Slate, woodland camo | L / D / M |
| 081 | Mallarcher (P3) | Engine | Compound bow with six stabilizer rods | Cold teal, matte black | L / D / M |
| 082 | Paintballer (P6) | Stalker | Electronic speedball marker with hopper | Slate, neon | L / D / M |
| 083 | Nerfer (P1) | Heckler | Neon-orange toy blaster with tactical rails | Mustard, neon orange | M / L / D |
| 084 | Spudgunner (P5) | Drifter | Shoulder-mounted PVC pipe cannon | Night blue, buffalo tan | M / L / D |
| 085 | Laserbro (P4) | Engine | Black aluminum laser emitter | Cold teal, electric blue | L / D / M |
| 086 | Slingshot (P2) | Heckler | Triple-tube steel-ball slingshot | Mustard, green | M / L / D |
| 087 | Candler (P3) | Firebrand | Multi-shot firework tubes held like pistols | Ember, neon sparks | M / L / D |
| 088 | Airhorn (P3) | Heckler | Dual brass compressed-air horn canisters | Mustard, brass | M / L / D |
| 089 | Ghillie (P1) | Stalker | Scoped hunting rifle wrapped in twine | Slate, burlap | M / L / D |
| 090 | Droner (P2) | Phantom | Hovering FPV quadcopter drone | Lavender, carbon | M / L / D |
| 091 | Plinker (P2) | Recluse | Lever-action metal air rifle | Moss, golden | M / L / D |
| 092 | Frogger (P3) | Showboat | Imaginary motorcycle handlebars (no held prop) | Peach, mottled blue | M / L / D |
| 093 | Oiler (P3) | Recluse | Handheld ultrasonic diffuser, lavender vapour | Moss, lilac | M / L / D |
| 094 | Bathwater (P6) | Leash | Sealed glass canning jar of glowing pink liquid | Rose, pink | L / D / M |
| 095 | Driver (P5) | Engine | Detached matte-black steering wheel | Cold teal, neon yellow | L / D / M |
| 096 | Lifehack (P6) | Engine | Hot glue guns on a canvas apron | Cold teal, rainbow | L / D / M |
| 097 | Uber (P1) | Engine | Phone on a vent mount, wicker basket of mints | Cold teal, mint | M / L / D |
| 098 | Widemouth (P4) | Showboat | Huge smile, a cardboard hand fan held at the chest | Peach, white | M / L / D |
| 099 | Keyboarder (P4) | Firebrand | Mechanical keyboard swung on a coiled cable | Ember, cool | M / L / D |
| 100 | Edgelord (P2) | Stalker | Dual folding steel karambits | Slate, purple | M / L / D |
| 101 | Gigaunit (P4) | Bulwark | Four stacked puffer jackets (worn) | Grey, frosty blue | M / L / D |
| 102 | Disheartened (P4) | Recluse | Crumpled receipt, half out of a pocket | Moss, charcoal | M / L / D |
| 103 | Pointing (P4) | Heckler | Yellow yardstick held across the chest | Mustard, blue | M / L / D |
| 104 | Krazed (P5) | Firebrand | Cracked beige CRT monitor held overhead | Ember, charcoal | M / L / D |
| 105 | Baconlover (P3) | Herald | Bundle of sizzling bacon strips | Soft cyan, warm | M / L / D |
| 106 | Gothgirl (P5) | Recluse | Black lace fan | Moss, black | M / L / D |
| 107 | Smugcat (P5) | Showboat | White porcelain plate of green salad | Peach, white | M / L / D |
| 108 | Snackvendor (P4) | Herald | Armful of chip bags and soda bottles | Soft cyan, neon green | M / L / D |
| 109 | Sealcommando (P3) | Stalker | Four-tube night-vision helmet | Slate, desert camo | M / L / D |
| 110 | Scammer (P1) | Leash | Coiled landline handset and wireless earpiece | Rose, bright blue | M / L / D |
| 111 | Preacher (P5) | Heckler | White megaphone and a leather-bound Bible | Mustard, charcoal | M / L / D |
| 112 | Scalper (P6) | Archivist | Mountaineering backpack of graphics-card boxes | Sepia, dark | L / D / M |
