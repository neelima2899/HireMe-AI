CSS = """
<style>
/* HireMe AI — light theme contrast fixes */

.stApp {
    background: #FAF9FF !important;
    color: #20243A !important;
}

.hero {
    background: linear-gradient(
        120deg, #FFFFFF 0%, #F3EEFF 100%
    ) !important;
    padding: 3rem 2.5rem !important;
    border-radius: 24px !important;
    margin-bottom: 2rem !important;
}

.hero-h1 {
    color: #1F2440 !important;
    font-size: clamp(2.4rem, 4vw, 3.6rem) !important;
    line-height: 1.12 !important;
}

.hero-h1 em {
    background: linear-gradient(
        90deg, #6D28D9, #4F46E5
    ) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.hero-p {
    color: #566179 !important;
    font-weight: 400 !important;
    max-width: 680px !important;
}

.hero-tag {
    color: #6D28D9 !important;
    background: #F0E9FF !important;
    border-color: #E5D9FF !important;
}

.hero-pill {
    color: #51466F !important;
    background: #FFFFFF !important;
    border: 1px solid #E7E1F1 !important;
}

.hero-deco {
    color: rgba(109, 40, 217, 0.035) !important;
}

.stTextArea textarea {
    background: #FFFFFF !important;
    color: #20243A !important;
    border: 1px solid #DDD8EB !important;
    border-radius: 14px !important;
}

.stTextArea textarea::placeholder {
    color: #8992A6 !important;
}

.stTextArea textarea:focus {
    border-color: #8B5CF6 !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}

.input-section-title {
    color: #555477 !important;
}

@media (max-width: 768px) {
    .hero {
        padding: 2rem 1.2rem !important;
    }
    .hero-deco {
        display: none !important;
    }
}
</style>
"""