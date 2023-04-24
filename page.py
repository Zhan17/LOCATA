from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("../Locata_Main.py", "Home", "🏠"),
        Page("pages/Analysis.py", "Page 2", ":books:"),
        Page("pages/Dashboard.py", "Page 3", ":books:")
        
    ]
)
