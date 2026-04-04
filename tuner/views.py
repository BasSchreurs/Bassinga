from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .audio_analyzer import AudioAnalyzer
from .threading_helper import ProtectedList
from .models import FretTab
import threading
import time
import json  # use lowercase

# --- AudioAnalyzer setup ---
note_queue = ProtectedList()
analyzer = AudioAnalyzer(note_queue)
analyzer.daemon = True  # allows it to exit when server stops
analyzer.start()

# Global variable to store the current note
current_note = "N/A"

# Thread to continuously update the current note
def update_note_thread():
    global current_note
    while True:
        freq = note_queue.get()
        if freq:
            current_note = analyzer.frequency_to_note_name(freq, 440)
        time.sleep(0.05)

threading.Thread(target=update_note_thread, daemon=True).start()


# --- Views ---
def home(request):
    return render(request, 'tuner/home.html')

def tuner_view(request):
    """
    Renders the tuner page with the selected fret tab (from GET parameter).
    """
    tab_id = request.GET.get('tab_id')  # GET parameter: ?fret_tab_id=123
    fret_tab_data = None
    song_name = None

    if tab_id:
        fret_tab_obj = get_object_or_404(FretTab, pk=tab_id)
        fret_tab_data = json.dumps({
            "G": fret_tab_obj.G,
            "D": fret_tab_obj.D,
            "A": fret_tab_obj.A,
            "E": fret_tab_obj.E
        })
        song_name = fret_tab_obj.name

    context = {
        "fret_tab": fret_tab_data,
        "song_name": song_name,
    }
    return render(request, "tuner/tuner.html", context)


def get_note(request):
    """
    Returns the current detected note as JSON for live JS updates.
    """
    return JsonResponse({"note": current_note})


def get_tab(request, tab_id):
    """
    Returns the fret tab content as JSON for JS update (if needed in future).
    """
    fret_tab = get_object_or_404(FretTab, pk=tab_id)
    return JsonResponse({
        "G": fret_tab.G,
        "D": fret_tab.D,
        "A": fret_tab.A,
        "E": fret_tab.E
    })


def selection_view(request):
    """
    Renders the song selection page with separate sections for each scale.
    Scale info is inferred from the prefix of the tab name (e.g., "Major - Song 1").
    """
    all_tabs = FretTab.objects.all()

    # Create separate lists for each scale by checking the name prefix
    natural_major_tabs = [tab for tab in all_tabs if tab.name.lower().startswith("natural major")]
    natural_minor_tabs = [tab for tab in all_tabs if tab.name.lower().startswith("natural minor")]
    major_pent_tabs = [tab for tab in all_tabs if tab.name.lower().startswith("major pentatonic")]
    minor_pent_tabs = [tab for tab in all_tabs if tab.name.lower().startswith("minor pentatonic")]
    blues_minor_tabs = [tab for tab in all_tabs if tab.name.lower().startswith("blues minor")]

    context = {
        "natural_major_tabs": natural_major_tabs,
        "natural_minor_tabs": natural_minor_tabs,
        "major_pent_tabs": major_pent_tabs,
        "minor_pent_tabs": minor_pent_tabs,
        "blues_minor_tabs": blues_minor_tabs,
    }

    return render(request, 'tuner/selection.html', context)
