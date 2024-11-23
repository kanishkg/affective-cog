
def calculate_intensity(emotion_percentages):
    """Average out the emotion percentages to get the intensity of each emotion"""
    # Assuming 100% is the maximum combined intensity for all emotions
    total_percentage = sum(emotion_percentages.values())
    intensities = {emotion: percent / total_percentage for emotion, percent in emotion_percentages.items()}
    return intensities

def map_emotion_to_AU(emotion, intensity):
    """Define the AU mapping for each emotion"""
    AU_mapping = {
        "Happiness": ["AU 6 (Cheek Raiser)", "AU 12 (Lip Corner Puller)"],
        "Sadness": ["AU 1 (Inner Brow Raiser)", "AU 4 (Brow Lowerer)", "AU 15 (Lip Corner Depressor)"],
        "Surprise": ["AU 1 (Inner Brow Raiser)", "AU 2 (Outer Brow Raiser)", "AU 5 (Upper Lid Raiser)", "AU 26 (Jaw Drop)"],
        "Fear": ["AU 1 (Inner Brow Raiser)", "AU 2 (Outer Brow Raiser)", "AU 4 (Brow Lowerer)", "AU 5 (Upper Lid Raiser)", "AU 20 (Lip Stretch)"],
        "Disgust": ["AU 9 (Nose Wrinkler)", "AU 15 (Lip Corner Depressor)", "AU 16 (Lower Lip Depressor)"],
        "Anger": ["AU 4 (Brow Lowerer)", "AU 5 (Upper Lid Raiser)", "AU 7 (Lid Tightener)", "AU 23 (Lip Tightener)"],
        "Contempt": ["AU 12 (Lip Corner Puller) on one side"]
    }
    aus = AU_mapping.get(emotion, None)
    if aus:
        return [f"{au} at {intensity} intensity" for au in aus]
    else:
        return f"No AUs mapped for {emotion}"

def process_text_and_map_AUs(emotion_percentages):
    """Parser for emotion percentages and mapping to AUs"""
    emotion_intensities = calculate_intensity(emotion_percentages)
    AU_results = {}
    for emotion, intensity in emotion_intensities.items():
        AU_results[emotion] = map_emotion_to_AU(emotion, intensity)
    return AU_results

def calculate_average_AU_intensity(AU_results):
    """Calculating the average intensity for each AU"""
    AU_intensity_sum = {}
    AU_count = {}

    for emotion, AUs in AU_results.items():
        for AU in AUs:
            # Extract AU name and intensity from the string
            parts = AU.split(' at ')
            if len(parts) == 2:
                AU_name = parts[0].strip()
                intensity = float(parts[1].split(' intensity')[0])

                # Summing up the intensities for each unique AU
                if AU_name in AU_intensity_sum:
                    AU_intensity_sum[AU_name] += intensity
                    AU_count[AU_name] += 1
                else:
                    AU_intensity_sum[AU_name] = intensity
                    AU_count[AU_name] = 1

    # Calculating the average intensity for each AU
    average_intensities = {AU: total_intensity / AU_count[AU] for AU, total_intensity in AU_intensity_sum.items()}
    return average_intensities