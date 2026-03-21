import Levenshtein  # pip install python-Levenshtein
import numpy as np

def compare_results(original_lines, dp_lines, random_lines):
    results = {
        "DP": {"exact": 0, "lev": []},
        "Random": {"exact": 0, "lev": []}
    }
    
    total = len(original_lines)
    
    for orig, dp, rnd in zip(original_lines, dp_lines, random_lines):
        if orig.strip() == dp.strip():
            results["DP"]["exact"] += 1
        if orig.strip() == rnd.strip():
            results["Random"]["exact"] += 1
            
        results["DP"]["lev"].append(Levenshtein.distance(orig, dp))
        results["Random"]["lev"].append(Levenshtein.distance(orig, rnd))
    
    print(f"{'Algorithm':<10} | {'Exact Match %':<15} | {'Avg. Edit Distance':<20}")
    print("-" * 55)
    for algo in ["DP", "Random"]:
        acc = (results[algo]["exact"] / total) * 100
        avg_edit = np.mean(results[algo]["lev"])
        print(f"{algo:<10} | {acc:<15.2f}% | {avg_edit:<20.2f}")

original_data = open("tadeusz_original.txt","r",encoding="utf-8").read().split("\n")
dp_output_data = open("tadeusz_output.txt", "r",encoding="utf-8").read().split("\n")
random_output_data = open("tadeusz_output_random.txt","r",encoding="utf-8").read().split("\n")
compare_results(original_data, dp_output_data, random_output_data)