exoticWords
===========

An exotic word generator.

This project seeks to play with phonologies of different languages, with the intention of creating a configurable generator that reflects the differing use of phonemes amongst languages/cultures.

<h2>Initial Project Outline</h2>

All humans share the contraints of the human mouth's possible shapes, which restricts total set of possible phones (spoken sounds). Languages are markedly different in the phonemes (meaningful combinations of phones) they employ, the combinations they are used permissably used in, the relative frequency of those various combinations and the graphemes (written forms) with which those phones are transcribed.

The first attempt of the project was simply to generate strings of letters which looks like they could feasibly be a person's name in an unknown foreign language; the sort of procedural content which might be useful for characters in a game world.

At first I was playing with a very simply programmatical generation of words by randomly selecting letters, having added a basic rule that vowels should almost always follow consonants, and visa versa. Generated results were interesting, but improved dramatically after a friend suggested the use of phonemes instead of stand-alone letters. I grabbed a simple list of transcribed phonemes so that now selections would include possiblities such as 'ou' and 'ie' to go along with single letters.

This project has been, since its initiation, a 'bottom-up' progression through linguistic features, attempting to improve generation quality with each new layer of complexity.

<h2>Expanded Project Outline</h2>



<h2>Transcription</h2>

The problem of transcription is firstly that many languages' written form (their 'orthographies'), are 'non-phonemic' (highly so in the case of English). While the shape and sound of a language is defined by its use of certain sets of phonemes, a language may not represent those phonemes each with written symbols. 'Shallow orthographies' use a near one-to-one mapping of phonemes to graphemes (a perfect mapping is a 'bijection'). 'Deep orthographies' are systems where the set of written forms diverge greatly from the set of phonemes used.

Indirect mappings between phonemes and their orthography can be explained by phenetic variation (over time, or across dialects) occuring more readily than orthography, which are often standardised (over both time and dialects). (Sidenote: generating phoneme information may cause some information to be lost if those phonemes share graphemes, or may exaggerate the frequency of a grapheme; a defect of this project).

**The scope of the ExoticWords project extends only to graphemes of the latin alphabet**, the letters used in English and other European languages. It seemed simplest that all generated content would be English-readable, mostly as a convenience to myself; the project involved a great deal of qualitative 'eye-balling' of generated 'words' in order to evaluate whether they could feasibly come from some particular language.

Transcribing all generated content into English presents large obstacles:
* English orthography is 'non-phonemic; the mapping of phonemes used in English to graphemes used in English is a 'deep orthography' with no perfect one-to-one correspondance. 
* There are many phonemes that are un-used in English: the harsh 'och' in Loch Ness is often stated as the single English use of that phoneme. 
* There are also phonemes which are used in English that are not reflected in English graphemes, such as the use of the glottal stop (excluded from explicit representation in many languages, but frequently represented in languages such as Classical Arabic).

Where phonemes may be rendered into multiple latin alphabet representations, such as 'sh' in English and 'sch' in German reprsenting the same phoneme, both representations will be possible for the generator: The goal of 'English-readable' generations does not necessitate English-only graphemes.

If phonemes are to be rendered as latin alphabet graphemes, then those which have no standard representation (in any latin alphabet language) become a problem. Such phonemes will be excluded from use in generations, sticking instead to phonemes which can be transcribed. Those rejected phonemes may later be re-incorporated if the project reaches a completed state and can be expanded to non-latin-alphabet graphemes, perhaps by listing sets of possible graphemes under their alphabet name, allowing alphabet selection prior to generation which then determines which phonemes can and cannot be used.

For those permissable phonemes, the earliest stages of this project have taken the liberty of pretending phonemes have singlular representations of a string of latin alphabet characters. As the project continued, automatic selection between multiple possible explicit graphemes associated with a given phoneme was implemented. In upcoming improvements, grapheme transcription may ultimately be determined on a syllabic level rather than phonetic.

Reference: 
http://en.wikipedia.org/wiki/Phonemic_orthography
http://en.wikipedia.org/wiki/Phoneme
http://en.wikipedia.org/wiki/Grapheme

<h2>Syllable Representation</h2>

<h2>Morphemes and Sentences</h2>

Generation of single words at a time may present a reader with some hallmarks of a novel language, but a language's distinctiveness also arises from its grammar: the patterns of word arrangement.

The scope of the Exotic Words project is not intended to cover Natural Language Processing so broadly that entire grammars will be recreated. That said, a mid-way addition to the project was simple functionality for generating mock 'paragraphs' of words.

The most basic form mimicks sentence structure by generating words of random lengths with a probability distribution that looks vaguely akin to that seen in european languages: many short words with occasional longer words.

A slightly more complex, but no less forced, approach may be used to provide systemic control of word length choices. A sentence should not be constructed only of long words, so a system to determine how long the next word should be, dependent on length of the most recent, is necessary. This may take on a markov chains quality of its own, a few basic 'word types' such as "long words", "short words" and "short connector words" (these are just crude possible examples). Each of these types would allow for small amounts of word length variation in themselves, but would all the enforcing of positional relationships between those types. 

Once syllable structures exist within the project, word length may be defined in syllabic terms (mono-syllabic, bi-syllabic etc).

'Morphemes' are the smallest grammatical units in a language, separated into two main categories:
* Free Morphemes: free-standing, independantly functioning words
* Bound Morphemes: mostly prefixes and suffixes
The incorporation of morphemes into sentence generation, in order to permit the explicit generation of bound-morphemes, may be implemented as a means to instate certain repeating letter sequences which are common in languages, such as the common prefix 'un-' in English.

Sentences, early in the project, were given a hard minimum length but were encouraged to vary slightly past this limit, with accompanying punctuation placed, therefore, largely at random. A small amount more variation in the approach may yield more interesting paragraph results, but this is not a focus of the project.

References: 
http://en.wikipedia.org/wiki/Morpheme

<h2>Information sources to investigate:</h2>

http://archives.conlang.info/pei/pirjhin/zurbhaunsaun.html

http://www.linguistics.ucla.edu/faciliti/sales/software.htm
http://www.phonetics.ucla.edu/vowels/contents.html

Hidden Markov Models, phonemes coding for multiple graphemes:
http://project.uet.itgo.com/markov_model.htm

Mention of positional probability:
http://iphodblog.blogspot.co.uk/ 
