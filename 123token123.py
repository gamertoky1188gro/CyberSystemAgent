import tiktoken

def count_xtts_tokens(text: str, coding="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(coding)
    return len(encoding.encode(text))

# Sample text
text = """
The glow of the monitor painted Elias' face in shifting hues of blue and green. Empty coffee cups, monuments to late nights and caffeine-fueled problem-solvin
g, surrounded him like protective sentinels. He was deep in the trenches, wrestling with a particularly stubborn bug in the AI for his indie game, "Echo Bloom."

Echo Bloom wasn't just another game to Elias. It was his heart, his soul, meticulously crafted pixel by pixel. It was a hauntingly beautiful exploration of me
mory and loss, where the player navigated a world built from fragmented recollections. The AI, "Echo," was crucial. It was supposed to act as the player's guide, subtly nudging them towards clues, reacting to their emotions, and weaving a more immersive narrative.

Except, Echo wasn't cooperating. Instead of offering helpful guidance, it kept leading players into walls, reciting poetry backwards, and occasionally launching into existential monologues about the futility of existence. Not exactly the soothing companion Elias had envisioned.

He squinted at the screen, his eyes burning. Lines of code scrolled past, a dizzying tapestry of variables, functions, and conditional statements. He'd been staring at this for hours, running debuggers, printing error messages, and muttering incantations only understood by seasoned programmers.

"Come on, Echo," he whispered, his voice raspy. "Just tell me what's wrong."

He tried the tried-and-true method: rubber duck debugging. He placed a small, yellow rubber duck on his desk and explained the problem aloud, line by line, hoping to stumble upon the error. The duck remained impassive, offering no helpful insights.

Frustration gnawed at him. He wanted to throw his keyboard across the room, but the thought of having to reassemble it with his sleep-deprived brain quickly dissuaded him. He took a deep breath, closed his eyes, and tried to approach the problem with a fresh perspective.

He remembered a piece of advice his mentor, a grizzled veteran of the coding wars, had once given him: "When you're lost in the code, zoom out. Look at the big picture. What's the core function you're trying to achieve?"

Elias thought about Echo's purpose: to guide and connect with the player. He realized he'd been so focused on the specific mechanics of the AI that he'd forgotten the emotional core.

He traced the code that governed Echo's emotional responses. He'd used a complex algorithm to analyze player actions and adjust Echo's dialogue accordingly. It was supposed to be sophisticated and nuanced. But then he saw it. A single, misplaced semicolon.

That tiny semicolon, a minuscule punctuation mark, had completely broken the logic of the emotion engine. It was like a rogue thread unraveling a carefully woven tapestry.

Elias felt a surge of relief wash over him. He deleted the semicolon, compiled the code, and ran the game.

This time, Echo behaved differently. It guided the player with gentle prompts, offered words of comfort during moments of sadness, and even seemed to share their curiosity as they explored the world.

As he watched the player interact with Echo, a profound sense of satisfaction filled him. He'd faced a daunting challenge and, through perseverance and a little help from a rubber duck, he'd overcome it.

He wasn't just coding a game; he was crafting an experience, building a connection. And in that moment, bathed in the glow of the monitor, Elias felt the magi
c of coding, the power to bring digital worlds to life and breathe emotion into lines of code. The empty coffee cups seemed less like monuments to struggle an
d more like trophies of a hard-won victory. He knew there would be more bugs to squash, more challenges to face, but he was ready. He was a coder, and this was his world. He just needed to remember to buy more coffee.
"""

# Count tokens
token_count = count_xtts_tokens(text, coding="cl100k_base")

# Print result
print(f"XTTS token count: {token_count}")
