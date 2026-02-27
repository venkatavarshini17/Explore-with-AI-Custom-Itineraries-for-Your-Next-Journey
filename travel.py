import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TravelGuide AI",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Gemini Pro Model
def initialize_gemini():
    """
    Initialize the Gemini Pro LLM with API key
    """
    try:
        # Get API key from environment variable or Streamlit secrets
        api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
        
        if not api_key:
            st.error("⚠️ Gemini API key not found. Please set GEMINI_API_KEY in your environment variables or Streamlit secrets.")
            st.info("👉 Get your API key from: https://makersuite.google.com/app/apikey")
            return None
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model
    
    except Exception as e:
        st.error(f"Error initializing Gemini Pro: {str(e)}")
        return None

# Generate travel itinerary
def generate_itinerary(model, destination, days, nights, interests=""):
    """
    Generate a personalized travel itinerary using Gemini Pro
    
    Args:
        model: Gemini Pro model instance
        destination: Travel destination
        days: Number of days
        nights: Number of nights
        interests: Additional preferences or interests
    
    Returns:
        Generated itinerary as string
    """
    try:
        # Create detailed prompt for the AI
        prompt = f"""
        Create a detailed and personalized travel itinerary for the following trip:
        
        Destination: {destination}
        Duration: {days} days and {nights} nights
        {f"Interests/Preferences: {interests}" if interests else ""}
        
        Please provide a comprehensive itinerary that includes:
        
        1. **Day-by-Day Schedule**: Break down activities for each day
        2. **Local Attractions**: Must-visit places and hidden gems
        3. **Dining Recommendations**: Local restaurants and cuisine to try
        4. **Accommodation Suggestions**: Areas to stay in
        5. **Transportation Tips**: Getting around the destination
        6. **Budget Estimates**: Approximate costs for activities
        7. **Travel Tips**: Important things to know (weather, customs, safety)
        8. **Best Time to Visit**: Each attraction
        
        Make the itinerary engaging, practical, and well-structured. Include specific timings and realistic schedules.
        """
        
        # Generate content using Gemini Pro
        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        st.error(f"Error generating itinerary: {str(e)}")
        return None

# Main Streamlit App
def main():
    # Header
    st.title("✈️ TravelGuide AI")
    st.markdown("### Your Personalized Travel Itinerary Generator")
    st.markdown("---")
    
    # Initialize Gemini Pro model
    model = initialize_gemini()
    
    if model is None:
        st.stop()
    
    # Sidebar for input
    with st.sidebar:
        st.header("🗺️ Trip Details")
        
        # Input fields
        destination = st.text_input(
            "Destination",
            placeholder="e.g., Paris, France",
            help="Enter your travel destination"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            days = st.number_input(
                "Days",
                min_value=1,
                max_value=30,
                value=5,
                help="Number of days"
            )
        
        with col2:
            nights = st.number_input(
                "Nights",
                min_value=0,
                max_value=30,
                value=4,
                help="Number of nights"
            )
        
        interests = st.text_area(
            "Interests & Preferences (Optional)",
            placeholder="e.g., History, Food, Adventure, Museums, Nature",
            help="Share your interests to get a personalized itinerary"
        )
        
        st.markdown("---")
        
        generate_button = st.button("🚀 Generate Itinerary", type="primary")
    
    # Main content area
    if generate_button:
        if not destination:
            st.warning("⚠️ Please enter a destination.")
        else:
            with st.spinner(f"✨ Generating your personalized itinerary for {destination}..."):
                # Generate itinerary
                itinerary = generate_itinerary(model, destination, days, nights, interests)
                
                if itinerary:
                    # Store in session state
                    st.session_state['itinerary'] = itinerary
                    st.session_state['destination'] = destination
    
    # Display itinerary if available
    if 'itinerary' in st.session_state:
        st.success(f"✅ Your itinerary for **{st.session_state['destination']}** is ready!")
        
        # Display the itinerary
        st.markdown("---")
        st.markdown(st.session_state['itinerary'])
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            # Copy button (using a text area for easy copying)
            if st.button("📋 Copy to Clipboard"):
                st.code(st.session_state['itinerary'], language=None)
        
        with col2:
            # Download button
            st.download_button(
                label="💾 Download Itinerary",
                data=st.session_state['itinerary'],
                file_name=f"{st.session_state['destination']}_itinerary.txt",
                mime="text/plain"
            )
    
    else:
        # Welcome message
        st.info("👈 Enter your trip details in the sidebar to generate a personalized travel itinerary!")
        
        # Feature highlights
        st.markdown("### 🌟 Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🤖 AI-Powered")
            st.write("Leveraging Google's Gemini Pro for intelligent itinerary generation")
        
        with col2:
            st.markdown("#### 🎯 Personalized")
            st.write("Tailored recommendations based on your interests and preferences")
        
        with col3:
            st.markdown("#### 📱 Easy Export")
            st.write("Download or copy your itinerary for offline access")

if __name__ == "__main__":
    main()