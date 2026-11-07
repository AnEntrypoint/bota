# Bota two-manifest verification report (FILLED)

Status: FILLED from one h.verify run with both real commit hashes. No placeholder tokens remain. Verification owned by the bota session; no spoint involvement.

## 1. Run metadata

| Field | Value |
| --- | --- |
| Report date | 2026-11-07 |
| Verifier | lanmower / bota session (self-verification) |
| Harness path | /tmp/bota-props-verify.mjs |
| Harness sha256 | 4960665b864f280b092a47f8167b77e89486dd0ef1b54a06355aeec14d193b4e |
| Invocation | const h = await import('/tmp/bota-props-verify.mjs'); return await h.verify(gm, {commits: ['deb29f534ef47116d41b92445fbc986f28213ebc','becc112b9a3710a91cd09c414667592ca9eec191']}); |
| Original manifest | /workspace/bota/docs/bota-props-2026-11-06.json |
| Original manifest sha256 | e3e0e9e9c6a19c2f123aeccf1c86f46b04f964237d4c29512aa6284cab4b3555 |
| Explicit manifest | /workspace/bota/docs/bota-props-explicit-2026-11-06.json |
| Explicit manifest sha256 | f98f1e3182f9d62188b5c462b8a5831eff816d682ffe4ad60f8cbb96e8281933 |
| Source prop list | /tmp/bota-needed-props.json - ef431bb9a5a587c6a507a105325beb03fd59f2bec88dbafce2be455cd8449175 |
| Source explicit list | /tmp/bota-explicit-props.json - c9017bf85974d6dbae0af8bdd3844254652fb9863c2c698d5f6fff06d8f7d910 |
| Commit 1 (original manifest) | deb29f534ef47116d41b92445fbc986f28213ebc |
| Commit 2 (explicit manifest) | becc112b9a3710a91cd09c414667592ca9eec191 |
| HEAD at run time | becc112b9a3710a91cd09c414667592ca9eec191 |
| origin/main at run time | becc112b9a3710a91cd09c414667592ca9eec191 |
| HEAD...origin/main divergence | 0	0 |

## 2. Overall verdict

| Result | Value |
| --- | --- |
| Overall verdict | PASS |
| Checks passed | 35 |
| Checks failed | 0 |
| Checks skipped | 0 |
| Total checks | 35 |
| Generated rows | 63 (expected 63) |
| Original true rows | 24 (expected 24) |
| Explicit rows | 39 (expected 39) |
| Held rows expected | 16 (expected 16) |
| Blocking failures | none |

Acceptance rule met: failed = 0, skipped = 0, generated rows = 63, and every GLB and commit check is PASS.

## 3. Generated rows (24 original true + 39 explicit)

| Harness check | Result | Detail |
| --- | --- | --- |
| source true rows = 24 | PASS | 24 |
| source held rows = 16 | PASS | 16 |
| source explicit rows = 39 | PASS | 39 |
| 24 true and 39 explicit slugs disjoint | PASS | [] |
| held/explicit overlap is owner-approved exception only | PASS | ["shop-npc-the-plug"] |
| original manifest present | PASS | "/workspace/bota/docs/bota-props-2026-11-06.json" |
| explicit manifest present | PASS | "/workspace/bota/docs/bota-props-explicit-2026-11-06.json" |
| original row count | PASS | {"actual":24,"expected":24} |
| original slug set matches | PASS | {"missing":[],"extra":[]} |
| original no duplicate slugs | PASS | [] |
| explicit row count | PASS | {"actual":39,"expected":39} |
| explicit slug set matches | PASS | {"missing":[],"extra":[]} |
| explicit no duplicate slugs | PASS | [] |
| gm.grep finds original manifest slug | PASS | {"slug":"base-morning-market","out":"/workspace/bota/docs/bota-props-2026-11-06.json:7       \"slug\": \"base-morning-market\",\n/workspace/bota/docs/bota-props-2026-11-06.json:8       \"outputGlb\": \"/wo"} |
| gm.grep finds explicit manifest slug | PASS | {"slug":"terrain-kit-lanes","out":"/workspace/bota/docs/bota-props-explicit-2026-11-06.json:6       \"slug\": \"terrain-kit-lanes\",\n/workspace/bota/docs/bota-props-explicit-2026-11-06.json:7       \""} |

Generated slug inventory: 63 unique slugs, listed in section 9.

## 4. Held rows (16 count-only / conflict categories)

| Harness check | Result | Detail |
| --- | --- | --- |
| 16 held rows held, 15 category slugs absent | PASS | none of the 15 category slugs appears in either manifest |

| # | Held row slug | Expected state | Observed state | Result |
| --- | --- | --- | --- | --- |
| 1 | terrain-kits-and-props | held | held, absent from both manifests | PASS |
| 2 | world-models-shop-and-drop | held | held, absent from both manifests | PASS |
| 3 | trend-costumes | held | held, absent from both manifests | PASS |
| 4 | trend-death-husks | held | held, absent from both manifests | PASS |
| 5 | out-of-bounds-marginalia | held | held, absent from both manifests | PASS |
| 6 | towers | held | held, absent from both manifests | PASS |
| 7 | content-mills | held | held, absent from both manifests | PASS |
| 8 | loading-dioramas | held | held, absent from both manifests | PASS |
| 9 | stockpile | held | held, absent from both manifests | PASS |
| 10 | lane-creeps | held | held, absent from both manifests | PASS |
| 11 | mega-creeps | held | held, absent from both manifests | PASS |
| 12 | stan-buffed-overlays | held | held, absent from both manifests | PASS |
| 13 | jungle-camp-creatures | held | held, absent from both manifests | PASS |
| 14 | shop-npc-the-plug | owner-approved exception | generated once as an explicit prop; absent from the original manifest | PASS |
| 15 | safe-spot | held | held, absent from both manifests | PASS |
| 16 | cosmetic-plinth | held | held, absent from both manifests | PASS |

Owner-approved exception note: shop-npc-the-plug is both a held row and one of the 39 explicit named slugs. It was generated exactly once in the explicit manifest (observed occurrences across both manifests: 1). No duplicate generation.

## 5. GLB checks (63 rows)

| Harness check | Result | Detail |
| --- | --- | --- |
| every row has a glb path | PASS | [] |
| every glb path is absolute | PASS | [] |
| every glb path under bota_prop_<slug> | PASS | [] |
| every row has a jobId | PASS | [] |
| every row has sha256 and byte count | PASS | [] |
| glb binary batch readable | PASS | 63 |
| glTF magic | PASS | {"badMagic":[],"binaryErrors":[]} |
| glTF version 2 | PASS | [] |
| declared length equals byte count | PASS | [] |
| manifest byte count matches file | PASS | [] |
| manifest sha256 matches file | PASS | [] |

Total GLB bytes read: 2000948996 (24-row batch 743,959,836 plus 39-row batch 1,256,989,160). All headers glTF, version 2, declared length equal to file size; all 63 manifest byte counts and sha256 digests matched the files in the harness run.

Per-row GLB ledger (63 rows):

| slug | manifest | absolute glb path | bytes | sha256 | jobId | magic | version | declared length | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base-morning-market | original | /workspace/hy3d/output/relay/bota_prop_base-morning-market/bota_prop_base-morning-market.glb | 31047696 | 8cd2567edc6525979f981d77cb0fcffd3cd493a237b7c264f23ac4e9448f3463 | 1510377400163172352 | glTF | 2 | 31047696 | PASS |
| base-late-night-market | original | /workspace/hy3d/output/relay/bota_prop_base-late-night-market/bota_prop_base-late-night-market.glb | 28805660 | 6b4f0cc49f8d1cb9dc30bfde9b8398c64884ca8a0539a8cd91fc850ad7a446e9 | 1510377400410636288 | glTF | 2 | 28805660 | PASS |
| spawn-lounge | original | /workspace/hy3d/output/relay/bota_prop_spawn-lounge/bota_prop_spawn-lounge.glb | 33914164 | 2370b1b6159d69322e8cdd2a908cc61698401927d38a1a1b62596b53bc66c5f1 | 1510377400528068608 | glTF | 2 | 33914164 | PASS |
| spawn-lounge-main-shop | original | /workspace/hy3d/output/relay/bota_prop_spawn-lounge-main-shop/bota_prop_spawn-lounge-main-shop.glb | 40773148 | 91ed26e19f2a2b6a4573dc34ef8d9ad0a7756bdde91083df63f9c98a28c805d4 | 1510379227822743552 | glTF | 2 | 40773148 | PASS |
| back-alley-shop | original | /workspace/hy3d/output/relay/bota_prop_back-alley-shop/bota_prop_back-alley-shop.glb | 32231152 | 18fadf74953e80f4229254546d89779ce594fd831aa96c50d256afec7379a737 | 1510378174347796480 | glTF | 2 | 32231152 | PASS |
| lane-stall-top | original | /workspace/hy3d/output/relay/bota_prop_lane-stall-top/bota_prop_lane-stall-top.glb | 35571196 | 2093632e5491e5168b3411b89f3a5ca8fa29607e5366e2505c092415bba70d5d | 1510383158992896000 | glTF | 2 | 35571196 | PASS |
| lane-stall-bottom | original | /workspace/hy3d/output/relay/bota_prop_lane-stall-bottom/bota_prop_lane-stall-bottom.glb | 33429092 | 37f96a0dde96a81cecf2839196cf646d692da76093c23f531c91a2d8eee3a322 | 1510379740484141056 | glTF | 2 | 33429092 | PASS |
| trend-pit | original | /workspace/hy3d/output/relay/bota_prop_trend-pit/bota_prop_trend-pit.glb | 23922036 | d23cd72c1ce7b75ca7313f0176ef2519b04c2e7c42bf807b20d74936c153560d | 1510378174171635712 | glTF | 2 | 23922036 | PASS |
| trend-base-model | original | /workspace/hy3d/output/relay/bota_prop_trend-base-model/bota_prop_trend-base-model.glb | 39973380 | 02f0b904bc442fa35bd6b592f85cc47f01be07f584830974a4ebb553020d25b1 | 1510386232755027968 | glTF | 2 | 39973380 | PASS |
| snapshot-pickup | original | /workspace/hy3d/output/relay/bota_prop_snapshot-pickup/bota_prop_snapshot-pickup.glb | 29893564 | 0efce7417a7d83d7f90b2b03d3491b63ea4ba872cf3b5ee62403bb0d7169b794 | 1510379227805974528 | glTF | 2 | 29893564 | PASS |
| delivery-drone-envelope-on-legs | original | /workspace/hy3d/output/relay/bota_prop_delivery-drone-envelope-on-legs/bota_prop_delivery-drone-envelope-on-legs.glb | 25416864 | 4ea6e21a583d622a1c0f41d54da8297e0228a4a3edbf1a7cc2a11b11ff55c590 | 1510379227889860608 | glTF | 2 | 25416864 | PASS |
| delivery-drone-flying-upgrade | original | /workspace/hy3d/output/relay/bota_prop_delivery-drone-flying-upgrade/bota_prop_delivery-drone-flying-upgrade.glb | 33310188 | 2233e8135e5577b54547e9ea6790a48eb2fcb962135d4f1c91a0b10c489ad8ed | 1510378692025573376 | glTF | 2 | 33310188 | PASS |
| coffee-drop | original | /workspace/hy3d/output/relay/bota_prop_coffee-drop/bota_prop_coffee-drop.glb | 26177056 | 3369b3b367eaf33b1b7be40aa95559be7bb9ee8cd9c7ee864e40859724b20a98 | 1510378729635905536 | glTF | 2 | 26177056 | PASS |
| breaking-news-zone | original | /workspace/hy3d/output/relay/bota_prop_breaking-news-zone/bota_prop_breaking-news-zone.glb | 32496264 | 6a56ba9ef377660b0a946ef159c6db81a6f569cb7ef6561310388ab34f23ed7e | 1510383158967721984 | glTF | 2 | 32496264 | PASS |
| marginalia-no-signal-tree | original | /workspace/hy3d/output/relay/bota_prop_marginalia-no-signal-tree/bota_prop_marginalia-no-signal-tree.glb | 31680680 | 902845507d76cc2bac3a0debdcce47fcd4e08654c961c4427fc608d6ca3355e0 | 1510390056106385408 | glTF | 2 | 31680680 | PASS |
| boost-sweat-mode | original | /workspace/hy3d/output/relay/bota_prop_boost-sweat-mode/bota_prop_boost-sweat-mode.glb | 32730536 | 0a585544534ca4a1dc4e877a43c8feb305111a372943490ccccdd65fa397f7b0 | 1510384477744979968 | glTF | 2 | 32730536 | PASS |
| boost-dank-goods-haste | original | /workspace/hy3d/output/relay/bota_prop_boost-dank-goods-haste/bota_prop_boost-dank-goods-haste.glb | 33850364 | 2da40afd5e6cf09fea11a9025cd619cf6d3989bf32ad349bb58f6c42f82446b7 | 1510383158988693504 | glTF | 2 | 33850364 | PASS |
| boost-dank-goods-illusion | original | /workspace/hy3d/output/relay/bota_prop_boost-dank-goods-illusion/bota_prop_boost-dank-goods-illusion.glb | 26520248 | 38d42832ebba50e941a36a603b5422f6619fee35d7a84eaca4d4d9f1a686aa8c | 1510384753625333760 | glTF | 2 | 26520248 | PASS |
| boost-dank-goods-invisibility | original | /workspace/hy3d/output/relay/bota_prop_boost-dank-goods-invisibility/bota_prop_boost-dank-goods-invisibility.glb | 20600280 | 018c984b88f5f8c13f2f557960134c73031c73e16e5920a33f125ff2e77078c5 | 1510390056102191104 | glTF | 2 | 20600280 | PASS |
| boost-dank-goods-regeneration | original | /workspace/hy3d/output/relay/bota_prop_boost-dank-goods-regeneration/bota_prop_boost-dank-goods-regeneration.glb | 27634080 | 9e64a063a30c3821de0f6c823639820439baefafbbf802df89d8ab7f4666ff94 | 1510381151724830720 | glTF | 2 | 27634080 | PASS |
| boost-bounty | original | /workspace/hy3d/output/relay/bota_prop_boost-bounty/bota_prop_boost-bounty.glb | 35559664 | ea3eab89189fd71d256fe55597359f1c7220c4da68b736f1d9cd0d23b5d5f37f | 1510392675294044160 | glTF | 2 | 35559664 | PASS |
| boost-demand | original | /workspace/hy3d/output/relay/bota_prop_boost-demand/bota_prop_boost-demand.glb | 32291912 | 3000719434f1da26f7b998e217106286fcd74d8c2ec18123685e411f44f58135 | 1510380413204357120 | glTF | 2 | 32291912 | PASS |
| ward-lurker-cam | original | /workspace/hy3d/output/relay/bota_prop_ward-lurker-cam/bota_prop_ward-lurker-cam.glb | 28968916 | a119d50fc31e3417a4f8dfb236152d3c0821b2e11407ca202c70f519164ff0a0 | 1510380847709085696 | glTF | 2 | 28968916 | PASS |
| ward-spoiler-tag | original | /workspace/hy3d/output/relay/bota_prop_ward-spoiler-tag/bota_prop_ward-spoiler-tag.glb | 27161696 | 8998303b2d54b034d4123ecc92df82576e44504263508d0563b2f0f93628f0f7 | 1510380866105303040 | glTF | 2 | 27161696 | PASS |
| terrain-kit-lanes | explicit | /workspace/hy3d/output/relay/bota_prop_terrain-kit-lanes/bota_prop_terrain-kit-lanes.glb | 29703944 | b75e438b49dbc20066de7dd7049fb7df787c77a2a46586dfdbebfe49a03f6909 | 1510388895940927488 | glTF | 2 | 29703944 | PASS |
| terrain-kit-jungle | explicit | /workspace/hy3d/output/relay/bota_prop_terrain-kit-jungle/bota_prop_terrain-kit-jungle.glb | 33032932 | e6b788009cb2484a44d94a0618b2c773e4d6de9bfe188eab2c9abca2599b7a7d | 1510388896310034432 | glTF | 2 | 33032932 | PASS |
| terrain-kit-river | explicit | /workspace/hy3d/output/relay/bota_prop_terrain-kit-river/bota_prop_terrain-kit-river.glb | 30253632 | 59e28294d3ce907a083b3380ce50699f37e5c65df254a3fea9dbef8168df0778 | 1510399618117074944 | glTF | 2 | 30253632 | PASS |
| hot-take-unironic | explicit | /workspace/hy3d/output/relay/bota_prop_hot-take-unironic/bota_prop_hot-take-unironic.glb | 28160128 | 971bfb1d17e39cf8e003c960f0092d57de3108a28612d824a0f3e628471269fa | 1510388896301645824 | glTF | 2 | 28160128 | PASS |
| gem-of-subtext | explicit | /workspace/hy3d/output/relay/bota_prop_gem-of-subtext/bota_prop_gem-of-subtext.glb | 32025556 | fb0e23a2cfe40634002dfad337183353473dbd57f8c2094ce0c282470595a33e | 1510389460662018048 | glTF | 2 | 32025556 | PASS |
| ticker-pin | explicit | /workspace/hy3d/output/relay/bota_prop_ticker-pin/bota_prop_ticker-pin.glb | 32504308 | 0e1f9538f8fa5cbcbb49fc48174028a973dba074f48f0951c71c69729c56a557 | 1510399618171592704 | glTF | 2 | 32504308 | PASS |
| crumb-pouch | explicit | /workspace/hy3d/output/relay/bota_prop_crumb-pouch/bota_prop_crumb-pouch.glb | 30012532 | 3e42f80b8122e3d75884bc59ad4ab6c784428b199673ee5341276b053e11a10c | 1510400137715843072 | glTF | 2 | 30012532 | PASS |
| npc-badge | explicit | /workspace/hy3d/output/relay/bota_prop_npc-badge/bota_prop_npc-badge.glb | 33446760 | f814d63a89c39a22e17a4914f42adaf7215b851953fa87459033909d9fa95a67 | 1510400910965145600 | glTF | 2 | 33446760 | PASS |
| echo-ring | explicit | /workspace/hy3d/output/relay/bota_prop_echo-ring/bota_prop_echo-ring.glb | 38631244 | 1bf608ee364a0ba521311d48f3a205db6ec3533e64eb6ea70d74abe71517ce40 | 1510401706138075136 | glTF | 2 | 38631244 | PASS |
| stan-sign | explicit | /workspace/hy3d/output/relay/bota_prop_stan-sign/bota_prop_stan-sign.glb | 30912424 | cb8ac71b82783bebd46cea490742dac5d8e3cf7dafee24eae0f31424ffe575cf | 1510392298389700608 | glTF | 2 | 30912424 | PASS |
| hot-mic | explicit | /workspace/hy3d/output/relay/bota_prop_hot-mic/bota_prop_hot-mic.glb | 27211916 | 00a09b91a9ff254b3a27af910901488e957f5b2fe357e7b787c91916a907d7b9 | 1510399618754600960 | glTF | 2 | 27211916 | PASS |
| ding-bell | explicit | /workspace/hy3d/output/relay/bota_prop_ding-bell/bota_prop_ding-bell.glb | 21600336 | a1f8d38474a451cbde818323eddcd9ae3618e199db90f7565b5f9f69920d8cff | 1510402025647562752 | glTF | 2 | 21600336 | PASS |
| thick-cloak | explicit | /workspace/hy3d/output/relay/bota_prop_thick-cloak/bota_prop_thick-cloak.glb | 25465520 | 3ebf924c51efa3fb45b100d6215dbc88be435866524786460104a802abf4a01f | 1510390056097996800 | glTF | 2 | 25465520 | PASS |
| cancel-mask | explicit | /workspace/hy3d/output/relay/bota_prop_cancel-mask/bota_prop_cancel-mask.glb | 26392360 | e757c62297aa4b223654a93e14407b9cb61fb293ea7573f8bd4d8a1bd721260e | 1510390580612489216 | glTF | 2 | 26392360 | PASS |
| eternal-ticker | explicit | /workspace/hy3d/output/relay/bota_prop_eternal-ticker/bota_prop_eternal-ticker.glb | 39536252 | 667b4354cf94716c11d430ed2d18b1a291ca53ecc3377f8a3aae28c973c22740 | 1510400910860279808 | glTF | 2 | 39536252 | PASS |
| vintage-lot | explicit | /workspace/hy3d/output/relay/bota_prop_vintage-lot/bota_prop_vintage-lot.glb | 31056940 | 83df5c450ddde26987e23564b3e5bfad44e5fd8cd9071998c1972accfb66180e | 1510393116144754688 | glTF | 2 | 31056940 | PASS |
| long-tail | explicit | /workspace/hy3d/output/relay/bota_prop_long-tail/bota_prop_long-tail.glb | 37606808 | 77604d668859f4d038f2361a5c4214bf51c76e47d57693538befc662a4b03fe7 | 1510400910847696896 | glTF | 2 | 37606808 | PASS |
| tower-tier1 | explicit | /workspace/hy3d/output/relay/bota_prop_tower-tier1/bota_prop_tower-tier1.glb | 37618616 | c35feaa27a773208b87b9154e6e27b1622c04dc573bbd61225d91829e722d9c0 | 1510401447848632320 | glTF | 2 | 37618616 | PASS |
| tower-tier2 | explicit | /workspace/hy3d/output/relay/bota_prop_tower-tier2/bota_prop_tower-tier2.glb | 32030044 | 8566c5be0af89697c2c260c5964075f29d2f2eca8fe6d788697599686b0dae7b | 1510401466093862912 | glTF | 2 | 32030044 | PASS |
| tower-tier3 | explicit | /workspace/hy3d/output/relay/bota_prop_tower-tier3/bota_prop_tower-tier3.glb | 31601336 | d4cb72eff30585be1560a05b8aaa0c58d5ba3dd3a8e5a1fd07edae9ff4a851fe | 1510402286969479168 | glTF | 2 | 31601336 | PASS |
| tower-tier4 | explicit | /workspace/hy3d/output/relay/bota_prop_tower-tier4/bota_prop_tower-tier4.glb | 30803200 | 5ef530e8ee54949b7265aec82940a0b8833c72c53716e7595d3230ad327035c1 | 1510391582581383168 | glTF | 2 | 30803200 | PASS |
| content-mill-melee | explicit | /workspace/hy3d/output/relay/bota_prop_content-mill-melee/bota_prop_content-mill-melee.glb | 32430612 | 9f9d6d1980f2b1f1db00f368851490e84140155e28bb55c6d4d3d188dac71003 | 1510402404422582272 | glTF | 2 | 32430612 | PASS |
| content-mill-ranged | explicit | /workspace/hy3d/output/relay/bota_prop_content-mill-ranged/bota_prop_content-mill-ranged.glb | 32452984 | 1fdd2b7313d510cb00989e44c4e6b1bb168ef2e9022f338324e22c776d1087b9 | 1510403126711083008 | glTF | 2 | 32452984 | PASS |
| creep-melee | explicit | /workspace/hy3d/output/relay/bota_prop_creep-melee/bota_prop_creep-melee.glb | 30746068 | 277b7d9031b454b89244e0931b383de429661f381847d4422a174ad37ba794bf | 1510392675285663744 | glTF | 2 | 30746068 | PASS |
| creep-ranged | explicit | /workspace/hy3d/output/relay/bota_prop_creep-ranged/bota_prop_creep-ranged.glb | 31178164 | 74bba052cd2b7b32d1ce98a8bd3ed7d9c4802bb4e943e05dac4f5655e2b86a69 | 1510402635897823232 | glTF | 2 | 31178164 | PASS |
| creep-siege | explicit | /workspace/hy3d/output/relay/bota_prop_creep-siege/bota_prop_creep-siege.glb | 28322420 | 13e7366b7a8de0bd6080b02bc15769307837badd222a477f4a6480ea8246161e | 1510403722860101632 | glTF | 2 | 28322420 | PASS |
| neutral-creature-background-npcs | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-background-npcs/bota_prop_neutral-creature-background-npcs.glb | 40282704 | e9e4095433ae472542ad44738e4d156a900d0eda1c0a0f96883bd1a317c7280a | 1510394520376770560 | glTF | 2 | 40282704 | PASS |
| neutral-creature-spam | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-spam/bota_prop_neutral-creature-spam.glb | 35052148 | d6ae8775d6dcca00fd5f25b1086edea1a46769b7db19dd0b80c8c30f8134bab3 | 1510393195115110400 | glTF | 2 | 35052148 | PASS |
| neutral-creature-scoffer | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-scoffer/bota_prop_neutral-creature-scoffer.glb | 38578900 | 209d5d83d9c820854bbaac965f4cc710563ea73a99d6f9653523b97085a89e23 | 1510395088474267648 | glTF | 2 | 38578900 | PASS |
| neutral-creature-troll-bridge | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-troll-bridge/bota_prop_neutral-creature-troll-bridge.glb | 31069968 | 51374ad0d20724da1fb9ddb0fa548c93fc9a8d523f82ac14639b462ac0c1a4dd | 1510394520980750336 | glTF | 2 | 31069968 | PASS |
| neutral-creature-old-forum-ticker | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-old-forum-ticker/bota_prop_neutral-creature-old-forum-ticker.glb | 34178320 | 72ecfe95f9a74d8528de10b5420efaf5a868b7defe1033194d2c08b858730b2b | 1510403737699549184 | glTF | 2 | 34178320 | PASS |
| neutral-creature-static-imp | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-static-imp/bota_prop_neutral-creature-static-imp.glb | 32811184 | 1079ecd3b7341b1d8d301a0c3a69d535531f25c054d87488b09d99c04c292683 | 1510393907102408704 | glTF | 2 | 32811184 | PASS |
| neutral-creature-ticker-sprite | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-ticker-sprite/bota_prop_neutral-creature-ticker-sprite.glb | 32364356 | 7b65932ddc7dc3e9e46bf4caa24fd7a9df181b9234f129dc31eb26c6ce9235f6 | 1510403869685899264 | glTF | 2 | 32364356 | PASS |
| neutral-creature-bio-bot | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-bio-bot/bota_prop_neutral-creature-bio-bot.glb | 32501168 | 92a534a7be1ddf7536c64bd97044ca320d6cad8ef24c11ee43d020182c879d76 | 1510395250936446976 | glTF | 2 | 32501168 | PASS |
| neutral-creature-reverb-wraith | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-reverb-wraith/bota_prop_neutral-creature-reverb-wraith.glb | 30600716 | 8037ce1224672b01af470465495e35a5d0ad5e9cec95bd44d7d8edbf2609e02b | 1510404437628215296 | glTF | 2 | 30600716 | PASS |
| neutral-creature-cancel-mob | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-cancel-mob/bota_prop_neutral-creature-cancel-mob.glb | 29471316 | 6aa488539ab516731d860cbccf9d2615c0d9a1a34b5e981356a7e4ffa5aad240 | 1510395339583062016 | glTF | 2 | 29471316 | PASS |
| neutral-creature-clang-golem | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-clang-golem/bota_prop_neutral-creature-clang-golem.glb | 32589368 | 88f68413753cdbfd0ac82bcc38b8f8497af0c834f89c37605c9337e855656006 | 1510404435891773440 | glTF | 2 | 32589368 | PASS |
| neutral-creature-markdown-hound | explicit | /workspace/hy3d/output/relay/bota_prop_neutral-creature-markdown-hound/bota_prop_neutral-creature-markdown-hound.glb | 38317560 | db1e5cc5fa989857804838a55839fb16467bcbe7cff89eb6b33dcae3caf61467 | 1510404363569397760 | glTF | 2 | 38317560 | PASS |
| shop-npc-the-plug | explicit | /workspace/hy3d/output/relay/bota_prop_shop-npc-the-plug/bota_prop_shop-npc-the-plug.glb | 34434416 | 372ccc75ee7a26332af66a404756526329f4e3f552dc8396875fd1e6bcad1fa5 | 1510405214266515456 | glTF | 2 | 34434416 | PASS |

## 6. Commit checks (two commits)

| Harness check | Result | Detail |
| --- | --- | --- |
| two distinct commit hashes provided | PASS | ["deb29f534ef47116d41b92445fbc986f28213ebc","becc112b9a3710a91cd09c414667592ca9eec191"] |
| author and committer lanmower | PASS | [{"hash":"deb29f534ef47116d41b92445fbc986f28213ebc","author":"lanmower","committer":"lanmower"},{"hash":"becc112b9a3710a91cd09c414667592ca9eec191","author":"lanmower","committer":"lanmower"}] |
| no trailers in commit messages | PASS | [{"hash":"deb29f534ef47116d41b92445fbc986f28213ebc","trailers":false,"message":"docs: manifest for 24 verified bota prop relay GLBs\n\n"},{"hash":"becc112b9a3710a91cd09c414667592ca9eec191","trailers":false,"message":"docs: manifest for 39 verified explicit bota prop relay GLBs\n\n"}] |
| both commits are ancestors of origin/main | PASS | [{"hash":"deb29f534ef47116d41b92445fbc986f28213ebc","ancestor":true},{"hash":"becc112b9a3710a91cd09c414667592ca9eec191","ancestor":true}] |
| each commit stages only its own manifest | PASS | {"original":["docs/bota-props-2026-11-06.json"],"explicit":["docs/bota-props-explicit-2026-11-06.json"],"all":[{"hash":"deb29f534ef47116d41b92445fbc986f28213ebc","changed":["docs/bota-props-2026-11-06.json"]},{"hash":"becc112b9a3710a91cd09c414667592ca9eec191","changed":["docs/bota-props-explicit-202 |
| no GLB or .env staged in either commit | PASS | ["docs/bota-props-2026-11-06.json","docs/bota-props-explicit-2026-11-06.json"] |
| committed manifest matches working tree | PASS | [{"hash":"deb29f534ef47116d41b92445fbc986f28213ebc","rel":"docs/bota-props-2026-11-06.json","committed":"e3e0e9e9c6a19c2f123aeccf1c86f46b04f964237d4c29512aa6284cab4b3555","working":"e3e0e9e9c6a19c2f123aeccf1c86f46b04f964237d4c29512aa6284cab4b3555"},{"hash":"becc112b9a3710a91cd09c414667592ca9eec191", |
| current index has no GLB or .env staged | PASS | [] |

| Field | Commit 1 | Commit 2 |
| --- | --- | --- |
| sha | deb29f534ef47116d41b92445fbc986f28213ebc | becc112b9a3710a91cd09c414667592ca9eec191 |
| author / committer | lanmower / lanmower | lanmower / lanmower |
| subject | docs: manifest for 24 verified bota prop relay GLBs | docs: manifest for 39 verified explicit bota prop relay GLBs |
| trailers | none | none |
| changed files | docs/bota-props-2026-11-06.json | docs/bota-props-explicit-2026-11-06.json |
| GLB or .env staged | none | none |
| committed manifest sha256 | e3e0e9e9c6a19c2f123aeccf1c86f46b04f964237d4c29512aa6284cab4b3555 | f98f1e3182f9d62188b5c462b8a5831eff816d682ffe4ad60f8cbb96e8281933 |
| working-tree manifest sha256 | e3e0e9e9c6a19c2f123aeccf1c86f46b04f964237d4c29512aa6284cab4b3555 | f98f1e3182f9d62188b5c462b8a5831eff816d682ffe4ad60f8cbb96e8281933 |

## 7. Failure register

No failures; all 35 checks passed. No blocking findings.

## 8. Evidence and sign-off

| Field | Value |
| --- | --- |
| Raw h.verify output | /tmp/bota-verify-result.json |
| GLB ledger evidence | /tmp/bota-verify-ledger.json |
| Harness self-test | standalone 12/12 PASS; gm mode 16/16 PASS |
| Fresh fetch performed | yes, before this verify run |
| HEAD / origin/main divergence | 0	0 |
| Repo edits made by verification | none |
| .env read | none |
| spoint involvement | none |
| Verified by | lanmower / bota session |
| Report delivered to | orchestrate |
| Delivery date | 2026-11-07 |

## 9. Generated slug inventory and filling record

| # | slug | manifest |
| --- | --- | --- |
| 1 | base-morning-market | original |
| 2 | base-late-night-market | original |
| 3 | spawn-lounge | original |
| 4 | spawn-lounge-main-shop | original |
| 5 | back-alley-shop | original |
| 6 | lane-stall-top | original |
| 7 | lane-stall-bottom | original |
| 8 | trend-pit | original |
| 9 | trend-base-model | original |
| 10 | snapshot-pickup | original |
| 11 | delivery-drone-envelope-on-legs | original |
| 12 | delivery-drone-flying-upgrade | original |
| 13 | coffee-drop | original |
| 14 | breaking-news-zone | original |
| 15 | marginalia-no-signal-tree | original |
| 16 | boost-sweat-mode | original |
| 17 | boost-dank-goods-haste | original |
| 18 | boost-dank-goods-illusion | original |
| 19 | boost-dank-goods-invisibility | original |
| 20 | boost-dank-goods-regeneration | original |
| 21 | boost-bounty | original |
| 22 | boost-demand | original |
| 23 | ward-lurker-cam | original |
| 24 | ward-spoiler-tag | original |
| 25 | terrain-kit-lanes | explicit |
| 26 | terrain-kit-jungle | explicit |
| 27 | terrain-kit-river | explicit |
| 28 | hot-take-unironic | explicit |
| 29 | gem-of-subtext | explicit |
| 30 | ticker-pin | explicit |
| 31 | crumb-pouch | explicit |
| 32 | npc-badge | explicit |
| 33 | echo-ring | explicit |
| 34 | stan-sign | explicit |
| 35 | hot-mic | explicit |
| 36 | ding-bell | explicit |
| 37 | thick-cloak | explicit |
| 38 | cancel-mask | explicit |
| 39 | eternal-ticker | explicit |
| 40 | vintage-lot | explicit |
| 41 | long-tail | explicit |
| 42 | tower-tier1 | explicit |
| 43 | tower-tier2 | explicit |
| 44 | tower-tier3 | explicit |
| 45 | tower-tier4 | explicit |
| 46 | content-mill-melee | explicit |
| 47 | content-mill-ranged | explicit |
| 48 | creep-melee | explicit |
| 49 | creep-ranged | explicit |
| 50 | creep-siege | explicit |
| 51 | neutral-creature-background-npcs | explicit |
| 52 | neutral-creature-spam | explicit |
| 53 | neutral-creature-scoffer | explicit |
| 54 | neutral-creature-troll-bridge | explicit |
| 55 | neutral-creature-old-forum-ticker | explicit |
| 56 | neutral-creature-static-imp | explicit |
| 57 | neutral-creature-ticker-sprite | explicit |
| 58 | neutral-creature-bio-bot | explicit |
| 59 | neutral-creature-reverb-wraith | explicit |
| 60 | neutral-creature-cancel-mob | explicit |
| 61 | neutral-creature-clang-golem | explicit |
| 62 | neutral-creature-markdown-hound | explicit |
| 63 | shop-npc-the-plug | explicit |

Filling record: this file was the blank template at sha256 034271eedcbded3a69bee4fdfc69268b8daeac9c9349e0bbffbb812c1b00ba9a and is now the filled report. All placeholders were replaced from one h.verify output; no placeholder tokens remain. The harness, both source /tmp JSONs, the contingency draft and the two manifests were not modified.

## 10. Owner decisions on the 16 held rows (2026-11-07)

The 16 rows with unambiguous:false are owner-decided in docs/bota-ambiguous-resolution.md: trend-costumes and trend-death-husks by the one-mesh decisions (commit 5a9b7ff), the other 14 by the fast-path decisions A3, B2, C3, C2 and D1. Every decision yields 0 new GLBs, 0 relay jobs and 0 bytes. Source: [fast-path dry run](/tmp/hy3d-bota-held-fast-path-dry-run.md) (6438 bytes, sha256 9723ef7bb047587a6d16502a87ae208a83145c725ac9d81d5d2262cf0a399bec).

Neither manifest changed: original sha256 e3e0e9e9c6a19c2f123aeccf1c86f46b04f964237d4c29512aa6284cab4b3555, explicit sha256 f98f1e3182f9d62188b5c462b8a5831eff816d682ffe4ad60f8cbb96e8281933. All 63 generated GLBs (2,000,948,996 bytes) are unchanged. No GLB, response.json, roster or script was created, deleted or changed. The verification result in sections 1-9 is unaffected.
