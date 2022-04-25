import csv

from tmdbv3api import TMDb, TV, Movie

tmdb = TMDb()
tmdb.api_key = "190fa2f501ae5442c7d317409a357059"  # Please dont use my api key
tmdb.language = "en"

filter = ["Animation", "Kids"]

movie = Movie()
tv = TV()

num_lines = sum(1 for line in open('NetflixHistory.csv')) - 1
print(num_lines)
file = open("NetflixHistory.csv", "a", newline="", encoding="utf-8")


csvout = csv.writer(file)

if num_lines == -1:
    csvout.writerow(["type", "title", "season", "episode", "duration", "genre", "date"])

with open('NetflixViewingHistory.csv', newline="", encoding="utf-8") as csvfile:
    token = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(token, None)
    for i, row in enumerate(token):
        if i < num_lines:
            print("skipping")
            continue

        show = row[0].split(":")
        title = ""
        if len(show) <= 2:
            title = row[0]
            print(title)
            search = movie.search(title)
            try:
                result = search[0].id
            except IndexError:
                print("Didnt find movie, searching for: ", title[:len(title)//2])
                search = movie.search(title[:len(title)//2])
                try:
                    result = search[0].id
                except IndexError:
                    print("Didnt find movie, skipping")
                    continue
            det = movie.details(result)

            for gen in det.genres:
                if gen.name in filter:
                    continue
                genre = gen.name
                break

            csvout.writerow(["movie", title, "", "", det.runtime, genre, row[1]])
        else:
            title = show[0].strip(" ")
            print(title)
            search = tv.search(title)
            result = search[0].id
            det = tv.details(result)

            try:
                duration = det.episode_run_time[0]
            except IndexError:
                duration = "15"

            for gen in det.genres:
                if gen.name in filter:
                    print("Filtered", gen.name)
                    continue
                genre = gen.name
                break

            csvout.writerow(["series", title, show[1].strip(" "), ":".join(show[2:]).strip(" "), duration, genre, row[1]])


file.close()
