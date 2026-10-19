"""Location intelligence with a search-driven, persistent map state."""
import folium
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

from app.components.cards import section_heading
from app.components.theme import apply_theme
from utils.location_score import calculate_location_score
from utils.maps import geocode_address, get_nearby_places

apply_theme()
section_heading("LOCATION INTELLIGENCE", "Search a neighbourhood, understand its everyday access", "Search any address, explore nearby amenities, and use a transparent score in your valuation.")

COLORS = {"school": "blue", "hospital": "red", "restaurant": "orange", "park": "green", "gym": "purple", "pharmacy": "cadetblue", "bank": "darkblue"}
SCORE_TYPES = ["school", "hospital", "restaurant", "park", "pharmacy"]

with st.form("location_search", border=False):
    address = st.text_input("Property address", placeholder="e.g. Koramangala, Bengaluru, India")
    left, middle, right = st.columns([2, 2, 1])
    with left:
        place_types = st.multiselect("Amenities to display", list(COLORS), default=["school", "hospital", "park"])
    with middle:
        radius = st.select_slider("Search radius", options=[500, 1000, 2000, 3000, 5000], value=2000, format_func=lambda value: f"{value / 1000:g} km")
    with right:
        submitted = st.form_submit_button("Analyse location", type="primary", use_container_width=True)

if submitted:
    if not address or not address.strip():
        st.error("Enter an address first.")
    else:
        with st.spinner("Locating address…"):
            try:
                lat, lng = geocode_address(address.strip())
            except Exception as exc:
                lat, lng = None, None
                st.session_state["location_geocode_error"] = str(exc)

        if lat is None or lng is None:
            st.error(
                "We couldn't find that address. Include the city and country, then try again. "
                f"({st.session_state.pop('location_geocode_error', 'no match returned')})"
            )
        else:
            # Only fetch what's actually needed: types the user wants to *see*,
            # plus the (usually small) set needed to compute the score, deduplicated.
            requested = set(place_types) | set(SCORE_TYPES)

            with st.spinner(f"Finding {len(requested)} amenity types from OpenStreetMap…"):
                places = {}
                progress = st.progress(0.0)
                for i, kind in enumerate(sorted(requested), start=1):
                    try:
                        places[kind] = get_nearby_places(lat, lng, kind, radius)
                    except Exception:
                        places[kind] = []
                    progress.progress(i / len(requested))
                progress.empty()

                score, breakdown = calculate_location_score(lat, lng, radius, places)

            st.session_state["location_analysis"] = {
                "address": address.strip(),
                "lat": lat,
                "lng": lng,
                "radius": radius,
                "display_types": place_types,
                "places": places,
                "score": score,
                "breakdown": breakdown,
            }

analysis = st.session_state.get("location_analysis")
if not analysis:
    st.info("Enter an address to start. Results remain visible while you compare valuation inputs or filters.")
    st.stop()

st.caption(f"Showing results for {analysis['address']} · {analysis['lat']:.4f}, {analysis['lng']:.4f}")
map_object = folium.Map(location=[analysis["lat"], analysis["lng"]], zoom_start=14, control_scale=True)
folium.Marker([analysis["lat"], analysis["lng"]], tooltip="Property location", icon=folium.Icon(color="red", icon="home", prefix="fa")).add_to(map_object)
cluster = MarkerCluster().add_to(map_object)
for kind in analysis["display_types"]:
    for place in analysis["places"].get(kind, []):
        folium.Marker(
            [place["lat"], place["lng"]],
            tooltip=f"{place['name']} · {place['distance_km']} km",
            icon=folium.Icon(color=COLORS.get(kind, "gray"), icon="info-sign"),
        ).add_to(cluster)
st_folium(map_object, use_container_width=True, height=480, key="estateiq_map", returned_objects=[])

score, breakdown = analysis["score"], analysis["breakdown"]
rating = "Excellent" if score >= 75 else "Good" if score >= 50 else "Developing"
a, b, c = st.columns(3)
a.metric("Location score", f"{score}/100")
b.metric("Access profile", rating)
c.metric("Coverage", f"{analysis['radius'] / 1000:g} km")
st.markdown("### Score breakdown")
for category, detail in breakdown.items():
    st.progress(detail["score"] / detail["max"], text=f"{category.title()}: {detail['found']} found · {detail['score']}/{detail['max']} points")

with st.expander("View amenity results"):
    for kind in analysis["display_types"]:
        items = analysis["places"].get(kind, [])
        st.write(f"**{kind.title()} ({len(items)})**")
        st.dataframe(items, column_config={"name": "Name", "distance_km": st.column_config.NumberColumn("Distance (km)", format="%.2f")}, hide_index=True, use_container_width=True)