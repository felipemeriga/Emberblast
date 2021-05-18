# Emberblast - Rule Book


## Attributes 

Each of the players will have a set of attributes that are used to help in during the
fight, in many aspects, they are:

- Health Points(HP): Represents the remaining life.
- Magic Points(MP): Used for casting magic.
- Move Speed: Determines how many tiles of the map the char is capable of moving.
- Strength: Used as base multiplier when inflicting physical damage.
- Intelligence: Used as base multiplier when inflicting magical damage.
- Accuracy: The probability that a user has to hit a target, also used as a plus damage factor for ranged attacks.
- Armour: Base multiplier to reduce physical damage taken.
- Magic Resist: Base multiplier to reduce magical damage taken.
- Will: Increases the probability of being the first to play in the turn, earn more xp and find an item.

Every time a user levels up, he will earn additional points, and will be able chose to distribute those points
into his attributes, just bear in mind that depending on the class, some attributes scale better than another.

Also, depending on the job and race you select, you will have additional attributes added in the beginning of the game,
so the combination of race/job, it can be crucial to achieve the most powerful scenario for your
character.

## Races

The game has some races available for you to select, but the best part is that the races are extendable and
customizable, which means that you can play the game as it is, with the default races, but you can also
change the configuration file, to create new races, or change the default races configurations.

The default races of the game are:
- Human: The honorable humankind, the most attributes balanced race.
- Dwarf: Kings of the mountains, are strong but slow.
- Elf: The wisdom and accuracy embraces this race.
- Orc: Directly from the dark cages, are strong and resistant.
- Halflings: The illustrious warriors of nimbleness, have a great speed and accuracy.


## Jobs

Like the races, the jobs are also customizable, jobs represents the class of the character, adding 
attributes and skills to it. The default classes are:

- Knight: The blessed warriors, very strong and resistant to damage.
- Wizard: Sages of the elements, intelligence and wisdom are their focus.
- Rogue: Masters of stealth, moves like an arrow with a good accuracy.
- Archer: The keepers of eagle's eyes, accuracy is their best friend.
- Priest: Guardians of holiness, intelligence and healing gaffers.

## Calculating Turn Order

The game is divided into turns, and in the beginning of each turn, the order of playing
will be calculated for all the players alive. The order is based on the following calculus:
```
Order = (Will / 10) * (Dice result)
```
So the players will be sorted according to the result of this formula, the highest values will
be first ones to play. 

Just remember that the dice can be configured in the configuration file of the game, you can select how many sides
the dice has, the default it's D20.

## How Does Physical Attack Damage is Calculated

The Physical damage can be either ranged or closed, the damage is calculated based in the following formulas:

- Closed Physical attack:
```
Damage = ((Strenght / 10) * (dice result)) + Critical Bonus
```
- Ranged Physical attack:
```
Damage = (((Strenght + Accuracy/5)/ 10) * (dice result)) + Critical Bonus
```



