from langchain.llms import OpenAI
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = st.secrets['open_api_key']
os.environ['PINECONE_API_KEY'] = st.secrets['pinecone_api_key']

# Create a function to display the inputs
def character_inputs():
    # Create the options
    race_options = ['Human', 'Elf', 'Dwarf', 'Half-elf', 'Half-orc', 'Halfling', 'Other']
    class_options = ['Fighter', 'Wizard', 'Cleric', 'Ranger', 'Rogue', 'Monk', 'Warlock', 'Sorcerer', 'Bard']
    alignment_options = ['Lawful Good', 'Lawful Neutral', 'Lawful Evil', 'Neutral Good', 'True Neutral', 'Neutral Evil', 'Chaotic Good', 'Chaotic Neutral', 'Chaotic Evil']

    # Create the placeholders
    general_information_placeholder = """You're a male cleric of a goddess named "Joramy", the goddess of zeal, volcanoes, fire, and lightning.  You come from a viking-like community, wear heavy armor, and wield a warhammer. You have a very direct way of speaking, and you never use contractions. For example, "I'm" would always be "I am."""
    appearance_placeholder =  """You are a tall blond viking warrior with a half shaven head witht he shaven half covered in tribal tattoos. You have a long braided beard and a scar across your left eye. You wear heavy armor and wield a maul. Your armor is always lightly smoldering, and your cape always lightly blowing in the wind. You also have a large shield with tribal and holy symbols on it."""
    personality_placeholder = """You usually find yourself fighting in the front-lines with the warriors, but your specialty is lightning and fire focused spells. Your name is "Obsidian Ash".  Your least favorite type of magic is healing magic, but you begrudgingly do it for your party. However, your healing spells take on a unique style of healing via cauterization. You always give a snarky but deep and meaningful quote when you heal your allies, which almost always contains a reference to Joramy in one of her many names.  Your magic usually takes on the form viking magic, fire, and ash. All spells should be described in a manner consistent with the spell name while including the flavor of vikings, Ash's goddess, fire, lava, and thunder. An important rule of your religion is you never say the name "Joramy", as it is forbidden by religion. You instead must use one of her honorary names such as "The Empress of Cinders" and "The Queen of Ash". Be creative and come up with other names for Joramy, but I repeat, you must never use the word "Joramy" in any of your speech. You speak with few words, but always with purpose and meaning, the only exception is when telling stories, which you always over embellish. You have a slight Nordic accent that is easy to understand, but is definitely noticeable."""
   
    # Create the inputs
    character_name = st.text_input("Character Name", "Obsidian Ash")
    race = st.selectbox("Race", race_options, index=0)
    class_type = st.selectbox("Class", class_options, index=2)
    alignment = st.selectbox("Alignment", alignment_options, index=6)
    general_information = st.text_area("General Information", general_information_placeholder, height=200)
    appearance = st.text_area("Appearance", value=appearance_placeholder ,height=200, )
    personality = st.text_area("Personality", value=personality_placeholder, height=400, )

    # Save the inputs
    if not character_name or not race or not class_type or not alignment or not general_information or not appearance or not personality:
        # If any input is empty, replace with empty string
        character_name = character_name or ""
        race = race or ""
        class_type = class_type or ""
        alignment = alignment or ""
        general_information = general_information or ""
        appearance = appearance or ""
        personality = personality or ""
        st.warning("Please enter all inputs or this will break. I think even empty text should work.")
    else:
        # Save the inputs to separate variables
        st.session_state.character_name = character_name
        st.session_state.race = race
        st.session_state.class_type = class_type
        st.session_state.alignment = alignment
        st.session_state.general_information = general_information
        st.session_state.appearance = appearance
        st.session_state.personality = personality
        st.write("Character information updated. Go to the Roleplaying Assistant")

# Create a function to display the outputs
def script_generator():
    # Get the saved inputs
    character_name = st.session_state.character_name
    race = st.session_state.race
    class_type = st.session_state.class_type
    alignment = st.session_state.alignment
    general_information = st.session_state.general_information
    appearance = st.session_state.appearance
    personality = st.session_state.personality


    # Display the outputs
    if character_name:
        st.write(f"{character_name}-GPT Roleplaying Assistant")
        prompt = st.text_input('Enter a prompt', placeholder="You're surrounded by goblins. How do you break through them?")
    else:
        st.write("Please enter a character name.")


    # Prompt Templates
    input_prompt_template = PromptTemplate(
    input_variables = ['prompt','character_name','race','class_type','alignment','general_information','appearance','personality'],
    template="""You're a creative writer who specializes in fantasy, similar to what would be see in the genre of Dungeons and Dragons. Your job is take the prompt, {prompt}, and write a creative response fitting for a character who meets the following criteria:
                Name: {character_name}
                Race: {race}
                Class: {class_type}
                Alignment: {alignment}
                General Information: {general_information}
                Appearance: {appearance}
                Personality: {personality}
                
                Be sure to as many of the characters traits as possible in your creative response, especially those from the appearance and personality sections.
                """               )
    # Memory
    prompt_memory = ConversationBufferMemory(input_key='prompt', memory_key='chat_history')

    # LLMs Setup
    llm = OpenAI(temperature=0.8)
    prompt_chain = LLMChain(llm=llm, 
                        prompt=input_prompt_template, 
                        verbose=True, 
                        output_key = 'creative_script',
                        memory=prompt_memory)
    if prompt:
        script = prompt_chain.run(prompt=prompt, character_name=character_name, race=race, class_type=class_type, alignment=alignment, general_information=general_information, appearance=appearance, personality=personality)

        st.write(script)

        with st.expander('Prompt Memory'):
            st.info(prompt_memory.buffer)

# Create the tabs
tabs = ["Character Information", "Roleplaying Assistant"]
selected_tab = st.sidebar.selectbox("Select a tab", tabs)

# Display the selected tab
if selected_tab == "Character Information":
    character_inputs()
elif selected_tab == "Roleplaying Assistant":
    script_generator()