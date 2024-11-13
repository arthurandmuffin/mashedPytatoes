from statistics import median

def medianFilter(list, windowSize):
    half_window = windowSize // 2

    filtered_list = []

    for i in range(len(list)):
        start_index = max(i - half_window, 0)
        end_index = min(i + half_window + 1, len(list))

        window = list[start_index:end_index]
        filtered_list.append(median(window))

    return filtered_list