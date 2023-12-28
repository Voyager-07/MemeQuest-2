from django.shortcuts import render
from django.db.models import Count
from .models import Meme
from .forms import MemeSearchForm
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_md")


def meme_search(request):
    if request.method == 'POST':
        form = MemeSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # print(search_query)
            # Process the search query with spaCy
            query_doc = nlp(search_query.lower())

            # Retrieve all memes from the database
            all_memes = Meme.objects.all()

            # Filter memes with at least some similarity
            # relevant_memes = [meme for meme in all_memes if
            #                   nlp(meme.title + " " + meme.metadata).similarity(query_doc) > 0]

            # Calculate similarity scores for each relevant meme
            for meme in all_memes:
                # meme_doc = nlp(meme.title + " " + meme.metadata)
                meme_meta = meme.metadata
                similarity_score = 0
                title_similarity = query_doc.similarity(nlp((meme.title).lower()))
                print(meme.title)
                print("Title Similarity : ",similarity_score)
                meta_phrase = [phrase.strip() for phrase in meme_meta.split(',')]

                # print(type(meta_phrase))
                # word_list = ''
                #
                # for phrase in meta_phrase:
                #     word = [p.strip() for p in phrase.split(' ')]
                #     word_list += word

                for phrase in meta_phrase:
                    ph = nlp(phrase)
                    similarity_score += query_doc.similarity(ph)
                print("Metadata Similarity : ", similarity_score-title_similarity)
                # similarity_score = query_doc.similarity(meme_doc)
                meme.similarity_score = similarity_score

            # Sort relevant memes by similarity score in descending order
            # relevant_memes = sorted(relevant_memes, key=lambda x: x.similarity_score, reverse=True)[:5]
            relevant_memes = sorted(
                all_memes,
                key=lambda x: (title_similarity, x.similarity_score),
                reverse=True
            )[:5]
            return render(request, 'home.html', {'memes': relevant_memes, 'form': form})
    else:
        form = MemeSearchForm()

    return render(request, 'home.html', {'form': form})
