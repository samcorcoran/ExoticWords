exoticWords
===========

An exotic word generator.

This project seeks to play with phonologies of different cultures, with the intention of creating a configurable generator that reflects the differing use of phonemes amongst languages/cultures.

<h2>Initial Project Outline</h2>



<h2>Expanded Project Outline</h2>



<h2>Transcription</h2>

The problem of transcription is firstly that many languages' written form (their 'orthographies'), are 'non-phonemic' (highly so in the case of English). While the shape and sound of a language is defined by its use of certain sets of phonemes, a language may not represent those phonemes each with written symbols. 'Shallow orthographies' use a near one-to-one mapping of phonemes to graphemes (a perfect mapping is a 'bijection'). 'Deep orthographies' are systems where the set of written forms diverge greatly from the set of phonemes used.

The scope of the ExoticWords project extends only to graphemes of the latin alphabet, the letters used in English and other European languages. It seemed simplest that all generated content would be English-readable, mostly as a convenience to myself; the project involved a great deal of qualitative 'eye-balling' of generated 'words' in order to evaluate whether they could feasibly come from some particular language.

Transcribing all generated content into English presents large obstacles. English orthography is 'non-phonemic; the mapping of phonemes used in English to graphemes used in English is a 'deep orthography' with no perfect one-to-one correspondance. What is more, there are many phonemes that are un-used in English: the harsh 'och' in Loch Ness is often stated as the single English use of that phoneme. There are also phonemes which are used in English that are not reflected in English graphemes, such as the use of the glottal stop (excluded from explicit representation in many languages, but frequently represented in languages such as Classical Arabic).

If phonemes are to be rendered as latin alphabet graphemes, then those which have no standard representation (in any latin alphabet language) become a problem. Such phonemes will be excluded from use in generations, sticking instead to phonemes which can be transcribed. Those rejected phonemes may later be re-incorporated if the project reaches a completed state and can be expanded to non-latin-alphabet graphemes, perhaps by listing sets of possible graphemes under their alphabet name, allowing alphabet selection prior to generation which then determines which phonemes can and cannot be used.

For those permissable phonemes, the earliest stages of this project have taken the liberty of pretending phonemes have singlular representations of a string of latin alphabet characters. As the project continued, automatic selection between multiple possible explicit graphemes associated with a given phoneme was implemented. In upcoming improvements, grapheme transcription may ultimately be determined on a syllabic level rather than phonetic.

Reference: 
http://en.wikipedia.org/wiki/Phonemic_orthography

<h2>Syllable Representation</h2>

<h2>Morphemes, Words and Sentences</h2>


References: 
http://en.wikipedia.org/wiki/Morpheme

Information sources to investigate:

http://archives.conlang.info/pei/pirjhin/zurbhaunsaun.html

http://www.linguistics.ucla.edu/faciliti/sales/software.htm
http://www.phonetics.ucla.edu/vowels/contents.html

Hidden Markov Models, phonemes coding for multiple graphemes:
http://project.uet.itgo.com/markov_model.htm

Mention of positional probability:
http://iphodblog.blogspot.co.uk/ 
