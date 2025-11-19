from openai import OpenAI
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


gemini_model = genai.GenerativeModel("gemini-2.5-flash")


# FIRE PROMPTS
fire_low = """Low Fire: Understanding Deficiency and Its Effects on Body and Mind
Low Fire leaves you feeling drained, unmotivated, and unable to push forward with confidence. Your inner spark dims, making tasks feel heavier and progress slower. Physically, you may experience sluggish digestion, cold hands and feet, weak muscles, low body heat, poor circulation, and frequent illness due to lowered immunity. Emotional symptoms include low courage, weakened self-esteem, and a depressive heaviness that makes it hard to start the day. The liver and gallbladder also function below capacity, contributing to low vitality and a sense of internal stagnation. This imbalance can make life feel overwhelming, but with consistent warming routines, you can rebuild strength, confidence, and momentum.

Ways to Boost Low Fire
Your goal is to gradually warm, energize, and stimulate the system so motivation and physical vitality return naturally over time.

Diet:
Incorporate warming spices and gentle sour foods to activate digestion and increase heat. Add lemons, yogurt, cayenne, cinnamon, cardamom, curry, ginger, and peppermint tea. Support liver and gallbladder function with herbs like burdock root and dandelion leaf to improve flow and metabolic energy.

Lifestyle and Exercise:
Choose regular movement that increases circulation and builds self-confidence. Aerobic exercise, hiking, skating, mountain climbing, or skiing all help strengthen your heart and rekindle drive. Surround yourself with fire colors—reds and oranges—in clothing or décor. Light candles or sit near a warm fire to absorb heat physically and energetically, encouraging the Fire element to rise.

Gems, Flower Remedies, and Aromas:
Use energizing crystals like carnelian, ruby, bloodstone, or topaz to stimulate motivation. Flower remedies such as Indian paintbrush and scarlet monkey flower help lift lethargy and spark emotional warmth. Uplifting scents like black pepper, basil, and cinnamon offer quick stimulation. In Chinese medicine, strengthening liver and gallbladder pathways helps restore Fire at its root.
"""
fire_high = """Assessing Your Fire Balance: Understanding Excess Heat and Its Impact
Excess Fire shows itself quickly when you know where to look—urine, skin, eyes, digestion, emotions, and immunity all reveal how intensely this element is burning within you. Dark or strong-smelling urine indicates the system is overheated, while skin may turn oily, reddish, inflamed, or prone to breakouts. Eyes become sharp or farsighted, reflecting heightened Fire activity. Digestion becomes hyperactive, creating intense hunger, excessive thirst, or diarrhea, with risks of deeper conditions like jaundice or hepatitis when the heat overwhelms organs. Emotionally, excess Fire manifests as irritability, impatience, aggression, or a short fuse that strains relationships and internal balance. Your immunity also becomes overly reactive, triggering fevers or inflammatory responses. What starts as vitality evolves into burnout: adrenal fatigue, migraines, ulcers, dehydration, and an inner pressure cooker that drains mental clarity and emotional softness. The Fire element is powerful—but when in excess, it pushes energy beyond sustainable limits.

Ways to Balance Excess Fire
Your goal is to cool, soothe, and regulate the intensity of Fire so the body and mind can maintain strength without damage.

Diet:
Choose cooling, hydrating foods that replenish moisture and calm inner heat. Favor cold water, lighter beers or cider, egg whites, soy milk, tofu, tempeh, cucumbers, melons, pumpkins, beans, mung beans, mangos, apples, sour pears, quinces, zucchini, spinach, tomatoes, salads, soft cheeses, seaweed, veal, pork, lamb, millet, mushrooms, and coconut or sunflower oil. Avoid dehydration by drinking steadily throughout the day, and reduce stimulating or heating foods.

Lifestyle and Exercise:
Engage in activities that cool rather than excite your system—swimming, mild baths, or gentle movement. Reduce intense sports, competitive pressure, and exposure to hot environments. Limit alcohol to light varieties and avoid emotional excesses that stoke the Fire further. A brief dry sauna session may help release excess heat, but avoid staying long enough to inflame the system. Incorporate blues and greens into your wardrobe, and use grounding crystals like green garnet, aventurine, calcite, aquamarine, emerald, or malachite. For emotional reactivity, Impatiens flower remedy helps ease anger and impulsivity. In Chinese medicine, supporting the kidneys helps regulate Fire and prevent overheating.

Herbal Support:
Use cooling, soothing herbs such as hops, violet, aloe, rhubarb, agrimony, dandelion, sorrel, water lily, groundsel, and mallows. These botanicals help reduce internal heat, calm inflammation, and restore fluid balance.

"""

# EARTH PROMPTS
earth_low = """Low Earth: What It Feels Like and How to Strengthen It
A deficiency of the Earth element loosens your natural grounding, leaving you unanchored and easily scattered. Daily life feels untethered—plans sound great in your head but fall apart when it’s time for real-world execution. You may drift between ideas, lose track of time, or appear unreliable to others. Physical awareness dims; meals become irregular or rushed, outdoor activity is avoided, and the body reflects this neglect through poor skin tone, fragile bones, and a general sense of depletion. Without Earth’s stabilizing accumulation, everything becomes fleeting and inconsistent, but this imbalance also signals the need to rebuild structure and cultivate steady habits.

Ways to Balance Low Earth
Restoring Earth requires grounding inputs—steady foods, routines, and environments that bring solidity back into your life. Strength returns when nourishment and rhythm become consistent.

Diet:
Choose warm, grounding, nutrient-dense foods that build and stabilize the body. Root vegetables such as carrots, potatoes, beets, squash, and turnips strengthen Earth’s foundation. Incorporate whole grains, brown rice, nuts, oils, cheese, butter, garlic, onions, and warming spices like ginger and curry. Support digestion with ginseng, pineapple, and fennel to bring energy downward and anchor the system.

Lifestyle and Exercise:
Create reliable rhythms—regular times for eating, sleeping, and unwinding—to reestablish stability. Engage with nature through gardening, walks in parks, or drives through natural landscapes to reconnect with the physical world. Earth tones such as greens and browns in clothing or home décor help induce a grounded state. Increase tactile awareness with weekly massages, and surround yourself with houseplants to reinforce environmental stability. Gemstones like malachite, emerald, chrysoprase, and aventurine offer additional anchoring support. Flower essences such as Clematis and manzanita enhance presence and grounded focus. In Chinese medicine, stimulating the heart and small intestine meridians—associated with Fire—can help strengthen Earth when it is depleted.

"""
earth_high = """Excess Earth – Characteristics & Symptoms
Excess Earth is marked by heaviness, density, and accumulation in both body and personality. Physically, the body becomes thick, compact, and resilient, showing a leathery quality in the skin along with greater body hair and slow-moving tissues. With continued buildup, issues such as sclerosis, calcium deposits, and structural congestion appear, creating a sense of sluggish heaviness throughout the system. Earth excess also contributes to a slow metabolism, reduced mobility, and a tendency toward feeling physically weighed down. Personality-wise, excess Earth reinforces strong practicality, material focus, and a need for control. You may feel deeply attached to routines, tradition, and predictability, valuing what is concrete and familiar. However, this grounding can tip into stubbornness, resistance to change, and difficulty accepting new perspectives or spiritual concepts. Emotional rigidity and mental heaviness can further block growth, making life feel static or overly serious without lightness or spontaneity.

What Excess Earth Feels Like
With too much Earth dominant in your chart, energy becomes stagnant. You may feel constantly tired, slow, or lethargic—like carrying extra weight that restricts your vitality. The body often trends toward a stocky or heavy build, not only from physical accumulation but also from reduced activity and difficulty initiating movement. Compulsive habits or fixations may emerge, especially around routines, body image, or material concerns. Digestion slows, leading to bloating, blockages, and a persistent feeling of heaviness. Accumulations can form in joints, vessels, or tissues, causing aches, reduced circulation, and metabolic congestion. This dominance behaves similarly to Water in its building tendencies, but when unchecked, it becomes stagnant and suffocating. The remedy lies in adding movement, warmth, and lightness—engaging the natural resilience of Earth without letting it harden or weigh down the system.

Diet:
Choose foods that are light, hydrating, and easy to digest, such as fruit salads, sprouts, fresh vegetables, and fiber-rich plant foods. Reduce reliance on dense, slow-moving foods like meats and potatoes, as they reinforce heaviness and stagnation. Space meals evenly to support slow digestion, and drink water throughout the day to maintain fluidity. To counteract cold and damp tendencies, incorporate warm and moist foods such as egg yolks, figs, olive oil, butter, raisins, and wheat products. Add nourishing items like spelt, turnips, carrots, beets, nuts, seeds, young cheeses, chicken, duck, rabbit, shrimps, shellfish, trout, and coconut. Red beet juice is especially beneficial for lifting melancholic Earth heaviness. Heating qualities can be added through spices, salt, cooking, or baking. Generally, spicy, sweet, and salty foods warm the system, while bitter and sour foods cool (with spicy-sour being heating).

Lifestyle and Exercise:
To counter Earth’s density, bring brightness and movement into your life. Surround yourself with stimulating colors such as yellow, gold, and orange to uplift the mood and energize the body. Engage in precision-based sports—tennis, golf, badminton, or similar activities—to activate agility and disrupt stagnation. Fresh air and breezy environments help stir circulation and lighten the system. Wearing fiery colors can naturally boost energy. Crystals like carnelian, hematite, rhodochrosite, and fire agate encourage activity and break up heaviness. Flower essences such as chestnut bud and chicory help release rigid patterns, while oak and mustard alleviate depressive Earth tendencies. In Chinese medicine, activating liver and gallbladder meridians supports flow and breaks accumulation.

Herbs:
Herbal allies for excess Earth include fumitory, polypody, senna, borage, lemon balm, dodder, scammony, and black hellebore—each helping lighten, cleanse, and disperse stagnation.
"""


# AIR PROMPTS
air_low = """
Low Air – Characteristics & Symptoms
A deficiency of the Air element expresses itself through reduced perception, introversion, fatigue, and noticeable slowness in both movement and mental processing. Individuals with low Air often experience shortness of breath and a diminished ability to interpret or express information clearly. Communication challenges are common, creating difficulty articulating thoughts, discomfort in social settings, and a reluctance to engage with others. Humor may feel inaccessible, and important decisions require extra contemplation due to slower cognitive flow. Physically, low Air disrupts the movement of energy through the body, resulting in poor circulation, reduced flexibility, and a sense of heaviness that amplifies lethargy and emotional withdrawal.

Remedies to Balance Low Air
Diet:
To invigorate the Air element, emphasize foods and beverages that energize and clarify the mind. Herbal teas such as gotu kola and fo-ti—celebrated in Chinese medicine for enhancing longevity—stimulate brain function and improve cognitive sharpness. Avoid heavy foods, as they increase bodily density and worsen low Air symptoms. Instead, incorporate raw fruits, vegetables, fresh juices, sprouts, and wholesome grains to introduce lightness and vitality into the system.

Lifestyle and Exercise:
Deep, conscious breathing practices are essential for restoring the Air element, improving lung capacity, and enhancing circulation. Spending time in elevated environments like mountains can be deeply revitalizing. Group activities support communication and social ease, while expressive movement practices such as dancing restore bodily awareness and lightness. Wearing sky-inspired colors like soft blue and coral gently stimulates Air qualities. Exposure to pleasant sounds or uplifting music further calms and nourishes this element.

Flower Essences and Energetic Remedies:
Flower essences such as Scleranthus, Sweet Pea, Quaking Grass, and Penstemon help develop adaptability, relational ease, and improved group connection. In Chinese medicine, supporting the stomach and spleen meridians is recommended to promote energy movement, improve vitality, and harmonize the Air element throughout the body.
"""


air_high = """Excess Air – Description
An individual with excess Air shows clear physical, digestive, movement-based, and mental signs of imbalance. The body becomes light, dry, and restless, often with a lean, wiry appearance and early aging due to loss of moisture. The skin is dry, veins stand out, and the person feels internally dehydrated. Digestion becomes irregular; hunger appears suddenly, digestion weakens, and the person requires frequent small meals. Low blood sugar, bloating, gas, and constipation are common, and severe imbalance can progress toward neurological or degenerative issues. Movements are fast and energy-consuming; joints may crack and sudden pains or spasms appear. Mentally, the Air-excess individual is highly active, overstimulated, talkative even during sleep, and uncomfortable with stillness or solitude. The mind absorbs information rapidly but struggles to process it deeply, causing fragmented memory, worry, fearfulness, and ungrounded thinking. Air governs circulation, communication, and the nervous system; when excessive, it destabilizes all three.

Excess Air – Psychological Effects
Excess Air creates sharp intelligence but emotional detachment and avoidance of bodily needs. The nervous system becomes overstimulated, producing jitteriness, anxiety, and nervous exhaustion. Apparent energy is deceptive—driven by unstable impulses rather than strength. Insomnia is common, especially waking between 2 a.m. and 6 a.m. The inability to stay still, aversion to solitude, and shallow processing of information amplify fear, worry, and inner instability.

Excess Air – Physical Manifestations
Surplus Air dries out the body, leading to rough skin, brittle hair and nails, and dehydrated tissues. Joint stiffness, spasms, cramps, and headaches arise due to an overloaded nervous system. Respiratory issues (like asthma) and circulatory weakness (including anemia) may appear. Digestive problems such as indigestion, flatulence, and constipation worsen over time. Toxic gas buildup can destabilize the gut-brain axis. Air imbalance intensifies with age, increasing risk of arthritis, paralysis, or spasms without correction.

Excess Air – Diet Recommendations
Favor grounding whole grains rich in B vitamins, green leafy vegetables high in magnesium, and calming teas such as chamomile, skullcap, vervain, and valerian. Peppermint tea supports digestion and muscle relaxation. Increase hydration with abundant water. Cold and dry foods that regulate Air include endives, potatoes, barley, lemon barley water, vinegar, lemons, sour oranges, rye, gooseberries, currants, sour apples and pears, chestnuts, lentils, medlar, tamarind, chicory, sprouts, vine leaves, barley coffee alternatives, beef, green olives, cauliflower, and broccoli.

Excess Air – Lifestyle and Exercise
Moderate exercise helps stabilize excess Air while reducing overall food intake to ease digestive strain. Avoid overstimulating social or mental activity. Favor grounding activities such as gardening and reduce exposure to rapid sensory input. Dry sauna sweating assists in releasing excess Air. Support the nervous system with gentle yoga, breathwork, and structured rest periods. Avoid overexposure to sun, strong winds, radiation from screens, and emotional shocks like fear.

Excess Air – Colors, Crystals, and Remedies
Deep blues and violets soothe the nervous system and calm circulatory overstimulation. Grounding contact with nature restores stability. Crystals and gems such as blue tourmaline, green calcite, chrysocolla, lapis lazuli, sapphire, and aquamarine promote mental peace. Nervine herbs including chamomile, catnip, skullcap, vervain, hops, and valerian help restore equilibrium. Flower remedies like white chestnut, mimulus, morning glory, and lavender are supportive. In Chinese medicine, warm spicy foods encourage circulation and improve digestion.

"""


# WATER PROMPTS
water_low = """Low Water: What It Feels Like and How to Restore Emotional Fluidity
Low Water weakens emotional flow, leaving you restless, anxious, and easily destabilized. You may find it difficult to understand or express your feelings, which creates emotional distance and reduces empathy. Suppressed emotions accumulate internally, leading to energetic blockages that manifest physically as brittle hair, fragile nails, dry skin, or issues related to dehydration. Without Water’s nourishing moisture, sensitivity fades and the intuitive, creative aspects of your nature become harder to access. Your body signals the deficiency through dryness, tension, and fearfulness, while your emotional landscape may feel shallow or disconnected. The invitation is to replenish, hydrate, and cultivate softness—to restore the element that supports emotional expression, intuition, and adaptability.

Ways to Balance Low Water
The goal is to reintroduce moisture, fluidity, and emotional expression through hydration, creativity, and environments rich in Water energy.

Diet:
Increase hydration with fresh spring water, vegetable juices, and nourishing herbal teas. Focus on moist, juicy foods such as watermelon, oranges, berries, cucumbers, leafy greens, and hydrating soups. Avoid excessive dry or dehydrating foods—crackers, chips, caffeine, and salt-heavy dishes—which further reduce Water energy. Favor gentle, hydrating nourishment that builds internal moisture and emotional softness.

Lifestyle and Exercise:
Spend time near natural or man-made bodies of water—lakes, rivers, pools, or the ocean—to absorb Water’s calming influence. Swimming or simply being immersed in water helps restore emotional flow and replenish Water energy. Engage in artistic expression—dance, painting, music, or other creative forms—to open emotional channels and reconnect with intuition. Maintain consistent hydration throughout the day to counter dryness and support emotional clarity.

Supportive Remedies:
Flower essences such as holly, sticky monkeyflower, fuchsia, garlic, and black-eyed Susan ease emotional blockage and support safe expression. Gemstones like pearl, tourmaline, and opal enhance creativity and emotional depth, while smoky quartz and black obsidian assist in releasing trapped emotions. In Chinese medicine, stimulating the lung and large intestine meridians (Air elements) can help enhance Water energy by restoring flow and circulation.

"""
water_high = """Excess Water: What It Feels Like and How to Bring Back Balance
Excess Water heightens emotional depth but can overwhelm you with dreaminess, moodiness, and a tendency to withdraw into your inner world. You may appear spacey, overly sensitive, or defensive as emotions swell beyond what the situation calls for. This imbalance increases vulnerability to depression, clinginess, and possessiveness driven by insecurity. Water’s subjective perception can distort reality, making it hard to stay grounded or objective. Physically, excess Water contributes to coldness, heaviness, fluid retention, and mucus buildup that affects the lungs, throat, and lymphatic system. You may experience recurring colds, allergies, phlegm, sluggish elimination, watery weight gain, or general lethargy as the body becomes waterlogged. Despite Water’s natural cleansing ability, the system becomes overloaded when its accumulation exceeds the body's metabolic fire.

Ways to Balance Excess Water
The path to balance involves adding heat, dryness, structure, and movement—evaporating what is excessive while strengthening inner warmth and clarity.

Diet:
Choose warm, dry, and lightly spiced foods that help evaporate moisture. Favor cooked meals over raw foods, and incorporate spices such as cayenne, ginger, mustard, horseradish, nutmeg, pepper, curry, and cinnamon to stimulate metabolism. Limit sweets, dairy, heavy salts, bread, and water-retaining foods like melons. Diuretic herbal teas—dandelion leaf, nettle, and alfalfa—support fluid release. Balance the heaviness of Water with lighter foods like dried fruits, crisp vegetables, and brittle snacks such as crackers or rice chips. Include hot and dry ingredients such as garlic, onions, paprika, winter radish, orange or lemon peel, parsley, carrots, fennel, asparagus, oats, basmati rice, salted fish, old cheeses, walnuts, hazelnuts, pistachios, and moderate red wine.

Lifestyle and Exercise:
Avoid cold environments and seek external heat sources like fireplaces, sunlight, or warm spaces. Fasting briefly can raise internal heat, while consistent moderate exercise keeps metabolism active without depleting energy reserves. Do not over-exercise; intense workouts consume the little internal heat available in water-dominant conditions. Saunas are highly beneficial, but sessions must be long enough to deeply warm the body and sweat out retained moisture. Limit oversleeping, and cultivate routines that encourage wakefulness and motion. Support emotional boundaries with psychic protection practices and grounding activities.

Supportive Remedies:
Flower essences such as honeysuckle, red chestnut, chamomile, clematis, and pink yarrow help soothe emotional hypersensitivity and strengthen boundaries. Crystals like rose quartz, kunzite, pink tourmaline, and green aventurine nurture emotional healing, while amethyst, fluorite, and sugilite elevate emotional clarity on a higher level. In Chinese medicine, stimulating the stomach and spleen meridians (Earth elements) can help regulate and counterbalance Water excess. Herbs such as elder, hyssop, thyme, spurge, briony, laurel, angelica, walnut, and broom assist with clearing dampness and improving metabolic warmth.
"""


# ==========================
#  ELEMENT LOGIC
fire_low_fixed = """The Fire Element:
The concept of the Fire element in traditional medicine systems aligns with several aspects of modern physiology and metabolism. The idea of "internal fire" (or Agni in Ayurveda) correlates with the body's basal metabolic rate (BMR), which is the amount of energy expended while at rest. A study published in the New England Journal of Medicine (1996) found that individuals with higher BMRs tend to have better cardiovascular health. This aligns with the traditional view that a balanced Fire element contributes to overall vitality.
The Fire element is all about that stimulating, creative energy that gets you moving and keeps things exciting. It handles your body heat, digestion, and the way sweat helps purify by flushing out toxins. When Fire is balanced in you, it shows up as solid physical energy and the drive to actually get things done—not just dream about them. You feel confident, cheerful, optimistic, courageous, inspired, warm, and affectionate toward others and yourself.
It also rules transformation and sight, both the physical kind and the psychological insight that helps you see things clearly. That means it controls internal processes like digestion, body temperature, and your immune system, which fights off threats. Fire drives all the chemical reactions that produce heat and light in your body. But if it builds up, it can create hyperacidity or excess bile in your small intestine, leading to infections or inflammation.
Fire makes you competitive and idealistic, with a real sense of fair play, but it's sensitive and can get thrown off by other elements. It's strongest from puberty to middle age, peaks around noon, in summer, and right after eating when digestion kicks in. Things like too much alcohol or constant excitement can make it unstable, and ignoring competition can dampen it down.
Physique: 
Lean or stream-lined with powerful muscles, often prominent veins, hirsute body, strong, expressive face, sparkling eyes.
Temperament: 
Choleric, bilious-nervous. Constitution: Athletic, ectomorphic.
What Low Fire Feels Like—and How It Holds You Back
Low Fire in your chart can leave you feeling wiped out, like everything takes more effort than it should. You're lethargic, low on courage or confidence, and self-esteem takes a hit—it's hard to believe in yourself when that inner drive just isn't there. Physically, vitality dips: poor digestion, a stiff body, cold hands and feet from bad circulation, weak muscles, indigestion, low body heat, and you're more prone to getting sick because your defenses are down. Your liver and gallbladder aren't pulling their weight, leading to sluggishness and that heavy depression where facing the day feels impossible. But this doesn't have to stick—you've got the power to warm things up and get that energy flowing again, one habit at a time.
Ways to Boost Low Fire:
Build it gradually with warming, energizing choices to get your spark back and face life with more fire.
Diet:
Add spices and sour foods slowly to wake up digestion and help your body absorb what it needs: lemons, yogurt, cayenne, cinnamon, cardamom, curry, ginger, or peppermint tea. Herbs like burdock root or dandelion leaf support your liver and gallbladder to get things moving.
Lifestyle and Exercise:
Get moving regularly; aerobic exercises to strengthen your heart and circulation, or solo challenges like hiking, mountain climbing, roller skating, ice skating, or skiing to build confidence and that "I can do this" feeling. Bring in red and orange colors in your clothes or space for an instant lift. Light candles or sit by a fire to tap into that warmth.
Gems, Flower Remedies, and Aromas Gemstones like carnelian, ruby, bloodstone, or topaz can amp up your energy. Flower remedies such as Indian paintbrush or scarlet monkey flower help shake off the lethargy. Scents like black pepper, basil, or cinnamon give a quick motivational hit. In Chinese medicine, work on your liver and gallbladder to fuel the Fire.
"""
fire_high_fixed = """
The Fire Element:
The concept of the Fire element in traditional medicine systems aligns with several aspects of modern physiology and metabolism. The idea of "internal fire" (or Agni in Ayurveda) correlates with the body's basal metabolic rate (BMR), which is the amount of energy expended while at rest. A study published in the New England Journal of Medicine (1996) found that individuals with higher BMRs tend to have better cardiovascular health. This aligns with the traditional view that a balanced Fire element contributes to overall vitality.
The Fire element is all about that stimulating, creative energy that gets you moving and keeps things exciting. It handles your body heat, digestion, and the way sweat helps purify by flushing out toxins. When Fire is balanced in you, it shows up as solid physical energy and the drive to actually get things done—not just dream about them. You feel confident, cheerful, optimistic, courageous, inspired, warm, and affectionate toward others and yourself.
It also rules transformation and sight, both the physical kind and the psychological insight that helps you see things clearly. That means it controls internal processes like digestion, body temperature, and your immune system, which fights off threats. Fire drives all the chemical reactions that produce heat and light in your body. But if it builds up, it can create hyperacidity or excess bile in your small intestine, leading to infections or inflammation.
Fire makes you competitive and idealistic, with a real sense of fair play, but it's sensitive and can get thrown off by other elements. It's strongest from puberty to middle age, peaks around noon, in summer, and right after eating when digestion kicks in. Things like too much alcohol or constant excitement can make it unstable, and ignoring competition can dampen it down.
Physique: 
Lean or stream-lined with powerful muscles, often prominent veins, hirsute body, strong, expressive face, sparkling eyes.
Temperament: 
Choleric, bilious-nervous. Constitution: Athletic, ectomorphic.
Assessing Your Fire Balance
To check how your Fire is doing, pay attention to your urine, skin color, eyes, digestion, emotions, and how well you fight off illness. These are straightforward signs your body gives you—listen to them so you can make changes before things get out of hand.
Urine: 
Light-colored urine often means low Fire, like your digestion isn't processing waste well. Dark, strong-smelling urine points to high Fire—your system's working overtime.
Skin: 
A rosy or red complexion is a good sign of normal or high Fire. Too much can mean oily skin, breakouts, pimples, inflammation, and a stronger body odor; you might not handle extra heat well because you're already running hot. Pale, cold, dry skin suggests low Fire.
Eyes: 
Bright, clear eyes show balanced Fire. Dull eyes or nearsightedness can mean it's low. Farsightedness is a clue to excess.
Digestion: 
With high Fire, you get super hungry fast after eating, feel thirsty a lot, and might have diarrhea—in bad cases, it could lead to jaundice or hepatitis. Low Fire means slow digestion, where food sits and ferments, causing gas, brain fog, headaches, and issues like diabetes or ongoing indigestion.
Emotions: 
Balanced Fire brings cheerfulness, optimism, and that spontaneous energy for things you care about. It's protective of its weak spots, though—push too hard, and snaps. Excess Fire ramps up anger, irritability, and aggression, which can hurt you or the people around you. Low Fire drains your self-esteem, motivation, confidence, and sense of well-being; it makes happiness feel out of reach and turns challenges into overwhelming burdens. Fire is what fuels real joy—without it, depression creeps in, and you start avoiding life.
Immunity: 
Fire gives you that fighter's edge to resist infections. Balanced, it keeps you strong. Too much overreacts with fevers and swelling. Too little leaves you wide open to getting sick more often.
What Excess Fire Feels Like—and Why You Need to Rein It In If you've got excess Fire in your chart, your physical energy is through the roof, and your digestion is firing on all cylinders—but it comes with a real risk of burning out. You push hard, feel that constant heat building, and before you know it, you're exhausted, dealing with adrenal fatigue from never letting up. All that strain wears on your body: high blood pressure that keeps you tense, migraines that hit like a truck, ulcers that remind you to slow down. You sweat a ton, get dehydrated easily, so you're always needing to drink more. And emotionally? You might snap with anger, get impatient and pushy, or get stuck thinking mostly about your own needs, which can leave you feeling isolated even when you're "winning."
The good news? You can shift this. Start noticing when you're overdoing - those signs are your body's way of saying, "Hey, let's pace this so you can keep going strong without crashing."
Ways to Balance Excess Fire Cool things down and add some moisture to offset the heat—small steps like these can make you feel steadier and in control.
Diet:
Go for cooling, hydrating foods to ease the intensity: lighter beers or cider, cold water, egg whites, milk or soy milk, whey, soybeans, tofu, tempeh, seitan, cucumbers, beans, peas, pumpkins, melons, mangos, apples, pears (sour ones are especially good), quinces, zucchini, spinach, tomatoes, salads, soft cheeses like cottage, unsalted pumpkin or melon seeds, fish (not trout), kelp and seaweeds, veal, pork, lamb, millet, mushrooms, sunflower or coconut oil. Drink plenty—dehydration sneaks up fast.
Lifestyle and Exercise:
Cool off with swimming or mild baths. Cut back on intense sports or competitions for a bit, limit alcohol to light beers, avoid hot environments and big emotional ups and downs. A short dry sauna can help sweat out the excess without overheating, just don't stay too long. Wear blues and greens to feel calmer. Gemstones like green garnet, aventurine, green calcite, aquamarine, emerald, or malachite can ground you. If anger flares quickly, try Impatiens flower remedy to smooth those edges. In Chinese medicine, support your kidneys to balance the heat.
Herbs:
Herbs like hops, violet, aloe, rhubarb, agrimony, dandelion, sorrel, water lily, groundsel, and mallows can help cool and soothe from the inside."""

earth_low_fixed = """The Earth Element:
The Earth element's association with stability and nourishment in traditional medicine systems has interesting parallels with modern nutritional science. The emphasis on whole grains and root vegetables for balancing Earth energy aligns with current dietary recommendations. A meta-analysis published in The Lancet (2019) found that diets rich in whole grains and fibrous vegetables are associated with reduced risk of colorectal cancer and improved digestive health.
 The concept of "grounding" in Earth element practices has been scientifically investigated. A study in the Journal of Environmental and Public Health (2012) found that direct physical contact with the Earth's surface (known as "earthing" or "grounding") can have measurable effects on inflammation, immune responses, wound healing, and prevention and treatment of chronic inflammatory and autoimmune diseases.
The Earth element is all about that dense, heavy grounding—solid and unyielding, like the soil that anchors everything in place. When it's balanced in you, it translates to practicality, unwavering stability, and a strong sense of responsibility that keeps your world steady. You step up as the caregiver and nurturer, offering that reliable support others crave, just as the earth sustains life without fanfare.
Physiologically, Earth is the builder: it governs your bones, teeth, skin, cartilage, muscles, tendons, and nails—the tough, structural elements that form the body's framework. Its core job is the formation and laying down of basic materials for construction, growth, maintenance, and repair of tissues. Just like Water, Earth accumulates steadily, gathering resources to fortify and endure. It is anabolic; that is, it builds up, creating density and strength over time. Tied to your sense of smell—for picking up scents or instinctively sensing threats—Earth is wired for survival, shining brightest in children as they grow strong and in the recovery phase after illness, when rebuilding takes center stage.
Temperament: Melancholic, lymphatic, nervous. Constitution: Solid, endomorphic.
Body Type and Personality: 
Signs of Your Earth Influence Earth equips you with hardy resilience and deep stamina—your body's go-to for long-haul endurance. In excess, that accumulation tips into overdrive: tissues densify, skin thickens to a tough, leathery feel, and you might see more body hair, along with sclerosis, calcium deposits, or a sluggish heaviness that weighs you down.
On the personality side, Earth keeps you grounded in the material world—cautious, tradition-loving, and all about respecting natural laws. You thrive on control and predictability, with that practical "small-shopkeeper" vibe that values the tried-and-true. But excess Earth can make you resistant to change or fresh ideas, especially anything spiritual or out-there, turning caution into a stubborn wall that blocks new growth.
What Excess Earth Feels Like—and Why It's Time to Lighten Up
With excess Earth loading up in your chart, you feel it in every step: a sluggish body bogged down by lethargy, like carrying an extra layer you didn't ask for. Your frame might trend stocky and heavy from all that building and accumulating—solid, sure, but often because exercise takes a backseat. Rigidity sets in, with compulsive habits (maybe fixating on your body or routines), and a slow metabolism that leads to blockages: joint deposits, artery clogs, heavy metal or calcium imbalances causing aches and congestion. Digestion drags, leaving you feeling stuffed and stuck. This buildup is your body's signal—it's tough and accumulative like Water, but unchecked, it stifles flow. The fix? Introduce some lift to keep that strength without the drag; you're resilient enough to adapt and thrive.
What Low Earth Feels Like—and How It Scatters You
Low Earth unravels that anchor, leaving you adrift: spacey or dreamy, with plans that sparkle in theory but crumble in the real world. You're seen as unreliable  -time slips away, practicality feels optional, and the tangible stuff (like deadlines or chores) gets sidelined. Body signals fade into the background: you eat haphazardly (on the run or skipped), dodge outdoor exercise or sun, and pay with poor skin tone or brittle bones that weaken without steady nourishment.
Without Earth's building accumulation, everything feels fleeting—but this is your invitation to root down, rebuild habits, and reclaim that grounded power. Diet tweaks and routines can stack up strength quickly.
Ways to Boost Low Earth:
Rebuild with grounding, nutrient-dense anchors—steady accumulation through food and rituals to make you feel solid and present again.
Diet: 
Eating heavy foods can ground you. These include root vegetables such as carrots, potatoes, turnips, beets, squash. You can also benefit by including whole grains, browned rice, nuts, oils, cheese, butter, garlic, onions and spices such as ginger and carry in your diet. Ginseng, pineapple and fennel can be helpful in stimulating digestion.
Lifestyle and Exercise: 
Establish anchors: a regular rhythm for eating, sleeping, and unwinding to foster reliability. Ground deeper with hands-on nature—gardening, park strolls, or countryside drives to reconnect. Earth tones like browns and greens in your clothes, houseplants everywhere, and more outdoor time pull you earthward. Weekly massages heighten body awareness and flow. Lean on green shades and gemstones like malachite, emerald, chrysoprase, or aventurine for tethering
Flower essences like Clematis and manzanita are recommended for grounding. In Chinese medicine, stimulating the heart and small intestine meridians, which are associated with the Fire element, can be beneficial in boosting the Earth element.
"""
earth_high_fixed = """The Earth Element:
The Earth element's association with stability and nourishment in traditional medicine systems has interesting parallels with modern nutritional science. The emphasis on whole grains and root vegetables for balancing Earth energy aligns with current dietary recommendations. A meta-analysis published in The Lancet (2019) found that diets rich in whole grains and fibrous vegetables are associated with reduced risk of colorectal cancer and improved digestive health.
 The concept of "grounding" in Earth element practices has been scientifically investigated. A study in the Journal of Environmental and Public Health (2012) found that direct physical contact with the Earth's surface (known as "earthing" or "grounding") can have measurable effects on inflammation, immune responses, wound healing, and prevention and treatment of chronic inflammatory and autoimmune diseases.
The Earth element is all about that dense, heavy grounding—solid and unyielding, like the soil that anchors everything in place. When it's balanced in you, it translates to practicality, unwavering stability, and a strong sense of responsibility that keeps your world steady. You step up as the caregiver and nurturer, offering that reliable support others crave, just as the earth sustains life without fanfare.
Physiologically, Earth is the builder: it governs your bones, teeth, skin, cartilage, muscles, tendons, and nails—the tough, structural elements that form the body's framework. Its core job is the formation and laying down of basic materials for construction, growth, maintenance, and repair of tissues. Just like Water, Earth accumulates steadily, gathering resources to fortify and endure. It is anabolic; that is, it builds up, creating density and strength over time. Tied to your sense of smell—for picking up scents or instinctively sensing threats—Earth is wired for survival, shining brightest in children as they grow strong and in the recovery phase after illness, when rebuilding takes center stage.
Temperament: Melancholic, lymphatic, nervous. Constitution: Solid, endomorphic.
Body Type and Personality: 
Signs of Your Earth Influence Earth equips you with hardy resilience and deep stamina—your body's go-to for long-haul endurance. In excess, that accumulation tips into overdrive: tissues densify, skin thickens to a tough, leathery feel, and you might see more body hair, along with sclerosis, calcium deposits, or a sluggish heaviness that weighs you down.
On the personality side, Earth keeps you grounded in the material world—cautious, tradition-loving, and all about respecting natural laws. You thrive on control and predictability, with that practical "small-shopkeeper" vibe that values the tried-and-true. But excess Earth can make you resistant to change or fresh ideas, especially anything spiritual or out-there, turning caution into a stubborn wall that blocks new growth.
What Excess Earth Feels Like—and Why It's Time to Lighten Up
With excess Earth loading up in your chart, you feel it in every step: a sluggish body bogged down by lethargy, like carrying an extra layer you didn't ask for. Your frame might trend stocky and heavy from all that building and accumulating—solid, sure, but often because exercise takes a backseat. Rigidity sets in, with compulsive habits (maybe fixating on your body or routines), and a slow metabolism that leads to blockages: joint deposits, artery clogs, heavy metal or calcium imbalances causing aches and congestion. Digestion drags, leaving you feeling stuffed and stuck. This buildup is your body's signal—it's tough and accumulative like Water, but unchecked, it stifles flow. The fix? Introduce some lift to keep that strength without the drag; you're resilient enough to adapt and thrive.
Ways to Balance Excess Earth:
Diet: 
Select light, quick-digesting foods to ease the load: fruit salads, sprouts, and fresh veggies. Cut back on dense ones like meat and potatoes that linger too long—space out meals to let digestion catch up, and sip water steadily to keep things flushing.
Warm and moist foods against excess earth: egg yolks, figs, olive oil, butter, raisins, white wine (and stronger beers), basil, wheat products, spelt, turnips, pods, carrots, red beets, nut and seeds (except those already mentioned above), grapes, blackberries, raspberries, soft younger cheese, duck, chicken, wild fowl, deer, doe, sheep, rabbit, shrimps and shell fish, trout, pomegranates, ghee (clarified butter), chickpeas, coconut. Red beet juice is strongly anti-melancholic, also spelt, wheat and white wine (which can be boiled to evaporate the alcohol).
Heat can be added to cold foods through hot spices, salt and by cooking and baking. In general spicy, sweet and salty foods have a heating quality, while bitter and sour foods are cooling (spicy-sour is heating though).
Lifestyle and Exercise: 
Infuse your surroundings with bright yellows, golds, and oranges to energize and dispel the weight. Try precision sports like tennis, golf, or badminton—they sharpen agility and bust through sluggishness without overwhelming your steady build. Chase fresh air and wind to stir circulation; fiery colors in your wardrobe give an easy pep. Crystals such as carnelian, hematite, rhodochrosite, or fire agate balance density with spark. 
Flower remedies like chestnut bud and chicory shake loose old patterns, oak and mustard ease depressive ruts. In Chinese medicine, activate liver and gallbladder (wood organs) through meridians to break up Earth's accumulation.
Herbs: fumitory, polypody, senna, borage, lemon balm, dodder, scammony, black hellebore."""

air_low_fixed = """
The Air Element:
The Air element's connection to respiration and the nervous system is well-supported by modern physiology. The emphasis on deep breathing exercises for those lacking in Air element aligns with scientific understanding of the benefits of controlled breathing. A study published in Frontiers in Psychology (2018) demonstrated that specific breathing practices can significantly reduce stress and anxiety levels, likely through modulation of the autonomic nervous system.
 The association between Air element imbalance and joint stiffness has been corroborated in modern rheumatology. Research published in Arthritis Research & Therapy (2015) shows that low humidity and sudden changes in barometric pressure (both air-related phenomena) can exacerbate joint pain in individuals with rheumatoid arthritis, supporting the traditional link between Air element and joint health.
The Air element, characterized by its inherent lightness, plays an essential role in facilitating movement throughout the body and mind.
 When well-balanced in an individual, it manifests graceful physical motion, clear and balanced perception, and effective communication skills. 
When in excess, it disrupts this harmony, amplifying restlessness and disconnection 
Physiologically, it governs circulation, the respiratory and nervous systems, overseeing all forms of connection—such as tubes, ducts, nerves, speech, touch, coordination, and propulsion. Importantly, the Air element does not directly control physical organs but rather the underlying principle of movement and interconnectedness within them. For instance, it regulates processes like peristalsis, bowel movements, sneezing, urination, and the rhythmic inflow and outflow of breath.
Temperament: 
Sanguine, bilious-sanguine. Constitution: Slender, ectomorphic.
Low Air: 
a lack of Air may lead to difficulties in perception, introversion, tiredness, shortness of breath, and slowness of movement. With a deficiency of air in the chart, you may have poor communication skills and a dislike of socializing. You can lack a sense of humor. You need to think things through more carefully before making an important decision. You may have a difficulty in the flow of bodily energies leading to poor circulation. Your body can lack elasticity and flexibility. 
Remedies to balance lack of Air
Diet: 
Herbal teas such as gotu kola or fo-ti, known as the "elixir of life" in Chinese medicine, can stimulate brain activity. Heavy foods should be kept to a minimum as they add to the heaviness of having low air. Eat plenty of raw fruits and vegetables. Juices, sprouts and grains should be added to the diet.
Lifestyle and exercise
Deep breathing exercises are essential. A trip to the mountains can be rejuvenating. Working with groups can enhance communication skills, while activities like dancing can increase awareness of movement through space. Wearing sky colours such as blue and coral can help. Pleasant sounds such as music can be calming and increase the air element. 
Flower remedies like Scleranthus, sweet pea, quaking grass, and penstemon can help one relate better to groups. In Chinese medicine, working with the stomach and spleen meridians is advisable to stimulate the Air element."""
air_high_fixed = """The Air Element:

The Air element's connection to respiration and the nervous system is well-supported by modern physiology. The emphasis on deep breathing exercises for those lacking in Air element aligns with scientific understanding of the benefits of controlled breathing. A study published in Frontiers in Psychology (2018) demonstrated that specific breathing practices can significantly reduce stress and anxiety levels, likely through modulation of the autonomic nervous system.
 The association between Air element imbalance and joint stiffness has been corroborated in modern rheumatology. Research published in Arthritis Research & Therapy (2015) shows that low humidity and sudden changes in barometric pressure (both air-related phenomena) can exacerbate joint pain in individuals with rheumatoid arthritis, supporting the traditional link between Air element and joint health.
The Air element, characterized by its inherent lightness, plays an essential role in facilitating movement throughout the body and mind.
 When well-balanced in an individual, it manifests graceful physical motion, clear and balanced perception, and effective communication skills. 
When in excess, it disrupts this harmony, amplifying restlessness and disconnection 
Physiologically, it governs circulation, the respiratory and nervous systems, overseeing all forms of connection—such as tubes, ducts, nerves, speech, touch, coordination, and propulsion. Importantly, the Air element does not directly control physical organs but rather the underlying principle of movement and interconnectedness within them. For instance, it regulates processes like peristalsis, bowel movements, sneezing, urination, and the rhythmic inflow and outflow of breath.
Temperament: 
Sanguine, bilious-sanguine. Constitution: Slender, ectomorphic.
Excess Air: 
An excess of the Air element in an individual can be readily observed by assessing key indicators: their physical appearance, digestive patterns, quality of movement, and level of mental activity. These signs reveal an imbalance characterized by excessive lightness, dryness, and restlessness, which can strain the body's systems over time.
Appearance: Individuals with excess Air often exhibit lean, wiry bodies that feel dry both internally and externally, with prominent, visible veins underscoring their delicate vascular structure. While they may retain a youthful vitality, their skin and overall appearance tend to age prematurely, showing early signs of dryness and fragility.
Digestion: Air-dominant types frequently feel disconnected from their bodily signals, unaware of hunger until it becomes intense and ravenous. Digestion is typically weak and irregular, necessitating small, frequent meals to maintain stability and counteract dehydration—they often feel parched and thirsty. Common issues include low blood sugar, bloating from flatulence, and chronic constipation. In prolonged cases, this imbalance can escalate to severe conditions like accelerated aging diseases, senility, convulsions, epilepsy, paralysis, or even mental instability.
Movements: Movements in those with excess Air are swift and agile, reflecting the element's nimble essence, but they consume energy rapidly due to hypersensitivity to external stimuli. Joints may creak audibly, accompanied by sudden shooting pains, muscle twitches, or spasms, signaling an overburdened nervous system.
Mental Activity: 
The mind of an Air-excess individual rarely rests, buzzing with constant activity—even manifesting as sleep-talking in the early morning hours. Highly strung and averse to stillness, they struggle to relax, flitting impulsively from one stimulus to the next with little self-restraint and a deep discomfort in solitude. While adept at rapidly absorbing new information, they falter in processing and integrating it deeply, leading to fragmented long-term memory. This superficial engagement fosters chronic fretting, worry, and anxiety, culminating in pervasive fearfulness and a profound lack of groundedness —making it challenging to anchor or apply acquired knowledge effectively.
The Air element governs circulation, the nervous system, respiration, and communication, embodying principles of movement and connectivity throughout the body and mind..
Excess Air: 
Psychological Effects
Excess Air endows sharp intelligence but often at the cost of emotional detachment and impersonality, as individuals rationalize away instinctive bodily needs in favor of logic. This fuels an overactive mind susceptible to nervous exhaustion, with a hyper-charged, ultra-sensitive nervous system that breeds jitteriness, anxiety, and unrelenting edginess. Apparent energy is illusory, sustained by erratic nervous impulses rather than enduring stamina, and compounded by an incessant mental hum that triggers insomnia—many drift off easily at night only to jolt awake between 2 a.m. and 6 a.m., unable to resettle. The aversion to solitude and impulsive stimulus-seeking further erode inner calm, while shallow information processing heightens vulnerability to fear and ungrounded worry.
Physical Manifestations of Excess Air
Physically, surplus Air depletes the body's moisture, yielding a lean, dehydrated frame prone to dry, rough skin; brittle hair and nails; and stiff, creaky joints. This desiccation overtaxes the nervous system, provoking tics, spasms, shooting pains, muscle cramps, and headaches, often alongside respiratory woes like asthma and circulatory issues such as anemia. Digestive disruptions—indigestion, flatulence, low blood sugar, and constipation—stem from poor instinctual attunement, with toxic gas buildup in the lower bowel disseminating unrest and impairing overall motility. Inflammatory conditions like arthritis and, in extremes, paralysis or convulsions may arise, particularly as Air's dominance intensifies with age, accelerating vulnerability to these degenerative patterns. Vigilance against dehydration is essential to mitigate progression.
Remedies to balance excess air
Diet: 
A diet rich in whole grains, which are grounding and contain most of the B complex vitamins, and green leafy vegetables, which are high in chlorophyll and magnesium, is recommended. Teas such as chamomile, skullcap, vervain and valerian can help calm the nerves. Peppermint tea can help both muscle spasms and digestive disorders. You need to increase your intake of fluids, especially water. 
Cold and dry foods to manage excess Air: 
endives, potatoes, barley, barley water with lemon juice, vinegar, lemons, and oranges (sour = cold/dry), rye, gooseberries, currants, sour apples, and pears (all sour fruits) chestnuts, lentils, medlar, tamarind, chicory, sprouts, vine leaves, surrogate coffee (chicory, oak, barley), beef, green olives, cauliflower, broccoli.
Lifestyle and Exercise Recommendations
To balance excess Air qualities, incorporate moderate exercise into your routine while reducing overall food intake to lighten the body's load. Limit stimulating social and mental activities, prioritizing rest and practical, grounding tasks like gardening to foster stability. Encourage the body to release excess moisture through sweating in a dry sauna. Support the nervous system with gentle practices such as yoga or deep breathing exercises, and ensure regular periods of rest and relaxation to allow it to recharge fully.
Factors That Aggravate Air Imbalance
Air qualities can intensify in dry, windy weather, as well as through overexposure to excess sunlight, X-rays, computer and television radiation, or emotional shocks like fear. The relentless influx of information and stimuli from media further exacerbates these effects, heightening restlessness and disconnection.
Soothing Colors and Nature Connection
Incorporate deep blue and violet hues into your environment to soothe and relax the overactive nervous system. Darker colors help calm excess blood flow, much like grounding yourself through direct contact with nature and the earth, which promotes a sense of rooted calm.
Crystals, Gems, and Herbal Remedies
For mental peace and nervous system equilibrium, work with crystals like blue tourmaline, green calcite, and chrysocolla, or gems such as lapis lazuli, sapphire, and aquamarine. Complement these with nervine herbal teas, including chamomile, catnip, skullcap, vervain, hops, and valerian, to gently ease tension and restore balance.
Flower remedies like white chestnut, mimulus, morning glory, and lavender are also recommended. In Chinese medicine, incorporating hot, spicy foods that promote circulation and digestion can be helpful."""

water_low_fixed = """
The Water Element
The Water element's association with emotions and fluids in the body has interesting correlations with modern psychoneuroimmunology. Research published in Molecular Psychiatry (2019) has shown that the gut microbiome, which is heavily influenced by hydration and fluid balance, plays a crucial role in regulating mood and emotional responses. This supports the traditional view of the Water element influencing emotional well-being.
 The emphasis on proper hydration for those lacking in Water element is well-supported by contemporary health science. A comprehensive review published in Nutrition Reviews (2010) highlighted the numerous health benefits of proper hydration, including improved cognitive function, physical performance, and thermoregulation, aligning with the traditional understanding of the Water element's importance.
The Water element is characterized by its cleansing and flowing nature. When balanced, it allows an individual to relate emotionally to others with proper empathy, without becoming overly subjective. It also enhances intuitive faculties and creative abilities. Physiologically, Water rules the lymphatic system and all the fluids in the body, including blood and various secretions. It softens and rounds out the body, providing smoothness and gentleness.
Water is most active in childhood, which is why catarrhal complaints are so common then. Water is the provider, both socially and physically, of cohesion. The quality of this relatedness falls somewhere between the stimulating, but superficial, light touch of air and the solid, unyielding attachment of earth. It flows into all interstices, lubricating and connecting.
Water rules the lymphatic circulation and all body fluids; it is anabolic, that is, it builds up, unlike fire, which breaks down through digestion. It is also associated with taste in all senses of the word, including the physical ability to distinguish flavour as well as the perception of good and bad taste in relation to both behaviour and aesthetics. Excess water can accumulate in the stomach and lungs as mucus, creating diseases of excess phlegm, fat and water in the rest of the body, such as oedema, asthma and bronchial disorders. Where water is low it is rather like excess air and is treated in the same way. The person is stiff, dehydrated and has difficulties in sleeping. There is a lack of softness and calmness.
Temperament: 
Phlegmatic, lymphatic, sanguine. Constitution: Endormorphic.
We can recognize Water presence by analyzing body type, voice and personality traits.
Body type: 
There is voluptuousness about the water type. The body is smooth, plump and soft, and the movements slow, flow and graceful. The hair is thick and plentiful, the eyes soft and melting. The sex drive is strong and the body temperature low. 
Voice: 
The water type tends to speak in a monotone, and one sentence runs into another without punctuation. 
Personality: 
When water is balanced the person is calm and unruffled. Its great gift is that of serenity. Water has an urgent need to protect itself and its own against the outside world.
Low Water: 
you tend to be restless, jittery anxious unstable at times and fearful. You may have difficulty understanding your own emotions and you could lack empathy. You can have problems showing emotions. Blocked emotions can lead to physical problems in the body that can cause an energy blockage. You can experience hair bones and brittle nails, or dry skin. Be careful with dehydration, drink fresh spring water. You need moist food, juicy fruits and vegetables. Joining a pool club or swimming pool can increase the water element, as well as an interest in the arts.
Remedies to balance low Water:
Diet: 
lacking in Water element, increasing fluid intake through vegetable juices and herbal teas is crucial.
Lifestyle and Exercise: Living near water and taking classes in arts can help express the intuitive and creative aspects of one's nature. 
Flower remedies such as holly, sticky monkey flower, fuchsia, garlic, and black-eyed Susan can help release and express emotions. Wearing gemstones like pearl, tourmaline, and opal can inspire creativity, while smoky quartz and black obsidian can aid in releasing emotions. In Chinese medicine, working with the lung and large intestine meridians (Air elements) can stimulate the Water element."""
water_high_fixed = """The Water Element:
The Water element's association with emotions and fluids in the body has interesting correlations with modern psychoneuroimmunology. Research published in Molecular Psychiatry (2019) has shown that the gut microbiome, which is heavily influenced by hydration and fluid balance, plays a crucial role in regulating mood and emotional responses. This supports the traditional view of the Water element influencing emotional well-being.
 The emphasis on proper hydration for those lacking in Water element is well-supported by contemporary health science. A comprehensive review published in Nutrition Reviews (2010) highlighted the numerous health benefits of proper hydration, including improved cognitive function, physical performance, and thermoregulation, aligning with the traditional understanding of the Water element's importance.
The Water element is characterized by its cleansing and flowing nature. When balanced, it allows an individual to relate emotionally to others with proper empathy, without becoming overly subjective. It also enhances intuitive faculties and creative abilities. Physiologically, Water rules the lymphatic system and all the fluids in the body, including blood and various secretions. It softens and rounds out the body, providing smoothness and gentleness.
Water is most active in childhood, which is why catarrhal complaints are so common then. Water is the provider, both socially and physically, of cohesion. The quality of this relatedness falls somewhere between the stimulating, but superficial, light touch of air and the solid, unyielding attachment of earth. It flows into all interstices, lubricating and connecting.
Water rules the lymphatic circulation and all body fluids; it is anabolic, that is, it builds up, unlike fire, which breaks down through digestion. It is also associated with taste in all senses of the word, including the physical ability to distinguish flavour as well as the perception of good and bad taste in relation to both behaviour and aesthetics. Excess water can accumulate in the stomach and lungs as mucus, creating diseases of excess phlegm, fat and water in the rest of the body, such as oedema, asthma and bronchial disorders. Where water is low it is rather like excess air and is treated in the same way. The person is stiff, dehydrated and has difficulties in sleeping. There is a lack of softness and calmness.
Temperament: 
Phlegmatic, lymphatic, sanguine. Constitution: Endormorphic.
We can recognize Water presence by analyzing body type, voice and personality traits.
Body type: There is voluptuousness about the water type. The body is smooth, plump and soft, and the movements slow, flow and graceful. The hair is thick and plentiful, the eyes soft and melting. The sex drive is strong and the body temperature low. 
Voice: The water type tends to speak in a monotone, and one sentence runs into another without punctuation. 
Personality: 
When water is balanced the person is calm and unruffled. Its great gift is that of serenity. Water has an urgent need to protect itself and its own against the outside world.
Excess Water: 
With an excess of water in the chart you can appear to others as dreamy and spacey. You're highly emotional and can become defensive at times. You are prone to depression and moodiness. You need to learn detachment. You need to use psychic self defence to avoid picking up negative vibrations around you. You can learn to channel your emotions in a positive way by getting involved in a creative project. Because water is cold, wet and heavy, an excess can contribute to phlegm and mucus discharges in the body which affect the lungs and throat. You may be prone to colds and lymphatic congestion. 
Excess water aids in eliminating toxins from the body, but you can become waterlogged and overweight. You are prone to diseases involving discharges or a buildup of fluids in the body. You can be overly sensitive to pollutants in the air, leading to allergies. 
Where there is excess water, it can lead to being overweight and laziness, but the weight is not due to fat; the body is simply waterlogged. Davidson suggests that over-watery people benefit from living by the sea and breathing salty air. This draws the water, by osmosis, out of the lungs and into the bronchial tree, where it can be coughed up and removed from the body.
When there is an excess or imbalance of water it can lead to greed, clinginess and possessiveness caused by insecurity. Everything is seen and valued subjectively, and this may be quite at odds with external reality and other people’s view of what is taking place. It is hard for water to be objective. The memory is retentive, which contrasts strongly with air which rules short-term memory.
Remedies to balance excess Water
Diet: 
The best we can do is evaporate water by eating warm and dry foods. It's recommended to eat mostly cooked foods with some spicy additions. Drinking diuretic herbal teas such as dandelion leaf, nettle, and alfalfa can be beneficial. The consumption of sweets and dairy products should be kept low. Foods that retain water, such as bread and salt, and especially melons, should also be kept at a minimum. The heaviness of water needs to be balanced by lighter foods such as dried fruits and salads and hot spices such as cayenne and ginger. Eating brittle foods that crumble, such as crackers and chips, helps reduce excess water.
Hot and dry foods against excess water: peppers, onions, garlic, ginger, curry, honey, horseradish, cinnamon, nutmeg, mustard, unrefined sugar, salt, (especially sea salt), winter radish, paprika powder, dried dates, walnuts, hazelnuts, pistachio nuts, parsley, radish, carrots, fennel, leeks, parsnips, asparagus, celeriac, orange and lemon peel, aniseed, old cheeses, artichokes, pure chocolate, aubergines, black olives, salted fish, maize, red wine, basmati rice, oats, goat meat, mutton, bacon, salt meats, all hot spicy foods.
Lifestyle and Exercise: 
You would benefit from avoiding cold, look for heat sources outside the body like a hearth fire, no bathing, fasting (heats you up), regular exercise to activate your metabolism. Don't sleep too long. Someone suffering from water excess should not exercise too much (and I have seen such cases!). Sport and competition consumes lots of heat, and in phlegmatic/water conditions there is not enough heat as it is, so we should not use it all up. Fanatical exercise will maintain the diseased, unbalanced condition. A sauna is useful but one must stay in the sauna for long, to really heat up and sweat out the excess moisture.
Flower remedies like honeysuckle, red chestnut, chamomile, clematis, and pink yarrow are suggested for emotional sensitivity and psychic protection. Crystals such as rose quartz, kunzite, pink tourmaline, and green aventurine are soothing and healing for the emotions, while amethyst, fluorite, and sugilite work with emotions on a higher plane. In Chinese medicine, working with the stomach and spleen meridians (Earth elements) can help control excess Water.
Herbs: 
elder, spurge, hyssop, thyme, briony, laurel, angelica, walnut, broom."""

# MODALITY DESCRIPTIONS (NOT SENT TO GEMINI)
# ============================================================

cardinal_description = """
Cardinal Energy
The Cardinal signs mark the beginning of each season: Aries (spring equinox), Cancer (summer solstice), Libra (autumn equinox), and Capricorn (winter solstice). The keyword associated with Cardinal signs is "Activity." 
Cardinal energy is characterized by action, duty, and responsibility. With the predominance of Cardinal planets in your chart, you tend to express through outward action and relationships, rather than through inner psychological scrutiny or adaptation to external circumstances.
Psychologically, an emphasis of planets in the cardinal signs in your chart, you can be demanding and willful. You're a troubleshooter, you like to be on the action, and you have a strong need to succeed. You like to solve problems through direct action. In fact, you propel yourself through life with such energy that you may overwhelm others, causing them to react in a negative manner toward you. A cardinal emphasis tends to rush you headlong into situations often without thinking and may try to push yourself beyond the limits of the body. There is a need to recognize your own limits and a need to for self-discipline and self-control. An excessive amount of cardinal energy can describe type A behavior. There is a need to slow down. 
The parts of the body that can be affected when you have most planets in cardinal signs include the chest area, stomach, rib cage, head, kidneys, bones, and gallbladder. You may find that some of your health problems are due to a weakness in the kidneys or gallbladder. Illness tends to be acute. When you do have a health problem, you're not afraid to try new treatments or medications. You're also impatient for results.
Remedies for Imbalance: practices that encourage introspection are beneficial. Meditation and reflection are important, as are physical disciplines like yoga and tai chi, which focus on inner awareness. Crystals such as amethyst, fluorite, and sugilite can be used to develop higher centers of consciousness.
Lacking Cardinal emphasis requires the need to engage more actively with the world and work with people. Martial arts, particularly aikido, can stimulate your energy. Crystals and gems like carnelian, jasper, hematite, rhodochrosite, ruby, and bloodstone can be helpful in boosting Cardinal energy.
"""

fixed_description = """
Fixed Energy:
The Fixed signs represent the middle of each season: Taurus (mid-spring), Leo (mid-summer), Scorpio (mid-autumn), and Aquarius (mid-winter). The keyword for Fixed signs is "Stability." Fixed sign energy tends to be stable and dependable but can also manifest as stubbornness and resistance to change.
Resistance to change can manifest stiffness in the body. Fixed illnesses can be cumulative in nature, resulting in growth, cysts, blockages, or enlargement of a body part. The body can be sluggish but can be helped with exercise. 
Body parts that can be affected are the throat, reproductive and eliminative organs, heart, and circulatory system. Problems with colon or thyroid gland. Consumption of heavy foods should be limited. 
Remedies for Imbalance: with excess energy in the Fixed modality often benefit from deep body therapies such as Rolfing and bioenergetics to break up old physical and emotional patterns. Flower essences like chicory, chestnut bud, fuchsia, black-eyed Susan, and trillium can be beneficial. Crystals like smoky quartz and black obsidian are also recommended.
When lacking Fixed energy physical disciplines that provide grounding are best, such as outdoor walks or running. You can work on developing willpower and following through with projects. Crystals like tiger's eye and hawk's eye can help ground higher energies into the body. Foods such as grains and root vegetables are also helpful in increasing Fixed energy.
"""

mutable_description = """
Mutable Energy:
The Mutable signs occur at the end of each season: Gemini (late spring), Virgo (late summer), Sagittarius (late autumn), and Pisces (late winter). The keyword for Mutable signs is "Flexibility." 
With most planets in the mutable signs in the chart, you are flexible and adaptable but tend to scatter your energies. You are people oriented and need a lot of mental stimulation. At times you become hyper and experience insomnia from trying to do too much at once. Many of your problems stem from an inability to relax or concentrate. You're easily distracted and are prone to anxiety or worry. There can be a mental component to your illness. You have some tendency toward hypochondria. Learning to finish one thing at a time before starting a new project will help calm your nervous system. 
You're prone to diseases that affect the lungs, intestines, nervous system and immune system. You're subject to sudden illness but usually have a quick recovery. However, there can be recurring illnesses. You may find that the cause of your illnesses relates to the lymph glands or pancreas. You need to build up your immune system and watch your sugar intake. 
Foods containing vitamins A/B and C and zinc aid the immune system. There can be metabolic disorders due to improper glucose production. There can also be illnesses difficult to treat, such as hypertension, ulcers and headaches. You can benefit from meditation, biofeedback or acupuncture. You need time to relax. Grounding techniques such as gardening or communing with nature, or disciplines that focus the attention, such as yoga and Tai chi, are beneficial. Flower remedies like white chestnut, madia elegans, Shasta daisy, vervain, and wild oat can work to focus and integrate energies. Crystals and gemstones like green calcite, aventurine, chrysoprase, chrysocolla, and malachite help ground energy.
When lacking Mutable emphasis, you can become rigid and crystallized in your attitude. Flowing movements, as in dance and tai chi, are helpful for the body. Flower essences such as rock water, quaking grass, and willow, as well as crystals like rose quartz, kunzite, and sugilite may be beneficial in increasing Mutable energy.
"""
# ============================================================
# ELEMENT PROMPT SELECTORS
# ============================================================

def build_fire_prompt(v):
    if v == 0:
        return ""
    if v > 28:
        return fire_high
    if v < 23:
        return fire_low
    return ""  # Balanced => NO PROMPT


def build_earth_prompt(v):
    if v == 0:
        return ""
    if v > 28:
        return earth_high
    if v < 23:
        return earth_low
    return ""  # Balanced => NO PROMPT


def build_air_prompt(v):
    if v == 0:
        return ""
    if v > 28:
        return air_high
    if v < 23:
        return air_low
    return ""  # Balanced => NO PROMPT


def build_water_prompt(v):
    if v == 0:
        return ""
    if v > 28:
        return water_high
    if v < 23:
        return water_low
    return ""  # Balanced => NO PROMPT
# ============================================================
# TITLE EXTRACTOR
# ============================================================

def extract_title(text):
    lines = text.strip().split("\n")
    for line in lines:
        if line.strip():
            return line.strip()
    return "Description"


# ============================================================
# BUILD DAILY PROMPT FOR GEMINI
# ============================================================

def build_final_prompt(fire, earth, air, water):
    p = ""
    p += build_fire_prompt(fire) + "\n\n"
    p += build_earth_prompt(earth) + "\n\n"
    p += build_air_prompt(air) + "\n\n"
    p += build_water_prompt(water)
    return p.strip()

def clean_json_output(text):
    text = text.replace("```json", "").replace("```", "")
    return text.strip()


# ============================================================
# DAILY ROUTINE GENERATION (GEMINI)
# ============================================================

def generate_daily_routine(user_input):
    fire = int(user_input["fire"])
    earth = int(user_input["earth"])
    air = int(user_input["air"])
    water = int(user_input["water"])

    element_prompt = build_final_prompt(fire, earth, air, water)

    system_prompt = """
You are AstraElements, an advanced Elemental Health AI.

rules to follow :
    -  Please create a daily plan - morning, midday and evening and apply each recommendation accordingly
    -  "Always generate the output as a complete daily schedule with clear time blocks "
    -  "(for example: '6:00–9:30 am', '10:00 am–4:00 pm', '7:00–10:00 pm'). "
    -  "Each block must contain specific actions, foods, exercises, environment cues, and behavior steps in chronological order. "
    -  "The routine must read like a real-world daily plan—morning, midday, and evening—with explicit timestamps and actionable steps, "
    - "never general advice."

Output ONLY valid JSON with this structure:

{
  "Morning": {
    "Diet": "...",
    "Lifestyle": "...",
    "Wear_Clothing": "...",
    "Exercise": "..."
  },
  "Midday": {
    "Diet": "...",
    "Lifestyle": "...",
    "Optional": "..."
  },
  "Evening": {
    "Diet": "...",
    "Lifestyle": "...",
    "Exercise": "..."
  },
  "Weekly_Addition": "..."
}

Each section must be ~100 words. No bullet points. Natural paragraph only.
No text outside JSON.
"""

    final_prompt = system_prompt + "\n\nUSER ELEMENT PROMPTS:\n" + element_prompt

    response = gemini_model.generate_content(final_prompt)
    cleaned = clean_json_output(response.text)

    try:
        return json.loads(cleaned)
    except:
        return cleaned


# ============================================================
# ELEMENT FIXED DESCRIPTIONS (High/Low)
# ============================================================

def build_descriptions_json(user_input):
    fire = int(user_input["fire"])
    earth = int(user_input["earth"])
    air = int(user_input["air"])
    water = int(user_input["water"])

    result = {}

    if fire > 28:
        title = extract_title(fire_high_fixed)
        result["Fire"] = {"Title": title, "Content": fire_high_fixed.strip()}
    if fire < 23:
        title = extract_title(fire_low_fixed)
        result["Fire"] = {"Title": title, "Content": fire_low_fixed.strip()}

    if earth > 28:
        title = extract_title(earth_high_fixed)
        result["Earth"] = {"Title": title, "Content": earth_high_fixed.strip()}
    if earth < 23:
        title = extract_title(earth_low_fixed)
        result["Earth"] = {"Title": title, "Content": earth_low_fixed.strip()}

    if air > 28:
        title = extract_title(air_high_fixed)
        result["Air"] = {"Title": title, "Content": air_high_fixed.strip()}
    if air < 23:
        title = extract_title(air_low_fixed)
        result["Air"] = {"Title": title, "Content": air_low_fixed.strip()}

    if water > 28:
        title = extract_title(water_high_fixed)
        result["Water"] = {"Title": title, "Content": water_high_fixed.strip()}
    if water < 23:
        title = extract_title(water_low_fixed)
        result["Water"] = {"Title": title, "Content": water_low_fixed.strip()}

    return result


# ============================================================
# MODALITY DESCRIPTIONS (ONLY HIGHEST)
# ============================================================

def build_modality_descriptions(user_input):

    cardinal = int(user_input["cardinal"])
    fixed = int(user_input["fixed"])
    mutable = int(user_input["mutable"])

    highest = max(cardinal, fixed, mutable)

    result = {}

    # Cardinal highest
    if cardinal == highest:
        t = extract_title(cardinal_description)
        result["Cardinal"] = {"Title": t, "Content": cardinal_description.strip()}

    # Fixed highest
    if fixed == highest:
        t = extract_title(fixed_description)
        result["Fixed"] = {"Title": t, "Content": fixed_description.strip()}

    # Mutable highest
    if mutable == highest:
        t = extract_title(mutable_description)
        result["Mutable"] = {"Title": t, "Content": mutable_description.strip()}

    return result


# ============================================================
# MASTER FUNCTION — FINAL OUTPUT
# ============================================================

def generate_complete_output(user_input):

    element_descriptions = build_descriptions_json(user_input)

    modality_descriptions = build_modality_descriptions(user_input)

    daily_routine = generate_daily_routine(user_input)

    final_json = {
        "Element_Descriptions": element_descriptions,
        "Daily_Routine": daily_routine,
        "Modality_Descriptions": modality_descriptions
    }

    return final_json


# ============================================================
# TEST RUN
# ============================================================

user_values = {
    "fire": 23,
    "earth": 23,
    "air": 18,
    "water": 36,
    "cardinal": 32,
    "fixed": 18,
    "mutable": 20
}

output = generate_complete_output(user_values)

print(json.dumps(output, indent=2))
