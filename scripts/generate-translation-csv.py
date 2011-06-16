from urllib import quote_plus, unquote
from pyango_view import str2img
import wikipydia
import re
import wpTextExtractor
import time
import os
import string
import codecs
import urllib
import editdist
import sys
import nltk.data
import csv
import bingtrans
import settings

def init_files(sentence_filename, article_filename):
    """
    Initalizes the sentence files (and the other parallel auxilary files).
    """
    output_file = open(sentence_filename, 'w')
    output_file.close()
    output_file = open(sentence_filename + ".google_translate", 'w')
    output_file.close()
    output_file = open(sentence_filename + ".tags", 'w')
    output_file.close()
    output_file = open(sentence_filename + ".seg_ids", 'w')
    output_file.close()
    output_file = open(sentence_filename + ".mask", 'w')
    output_file.close()
    output_file = open(article_filename, 'w')
    output_file.close()
    output_file = open(article_filename + ".ids", 'w')
    output_file.close()
    output_file = open(article_filename + ".target_titles", 'w')
    output_file.close()


def write_lines_to_file(output_filename, lines):
    """ Appends a list of lines to file. """
    output_file = open(output_filename, 'a')
    for line in lines:
        output_file.write(line.encode('UTF-8'))
        output_file.write('\n'.encode('UTF-8'))            
    output_file.close()
    return lines


def read_lines_from_file(filename, encoding='utf8'):
   """ Reads a file in utf8 encoding into an array """
   lines = []
   input_file = codecs.open(filename, encoding=encoding)
   for line in input_file:
      lines.append(line.rstrip('\n'))
   input_file.close()
   return lines



def get_translations(sentence_filename, sourceLang, targetLang="en", write_to_file=True):
    sentences = read_lines_from_file(sentence_filename)
    translations = []
    if sourceLang == "ur":
        for i in range(0, len(sentences)): translations.append(u"")
        translations = write_lines_to_file(sentence_filename + ".google_translate", translations)
    else:
        for sentence in sentences:
            translation = ''
            try:
                translation = bingtrans.translate(sentence, sourceLang, targetLang)
            except ValueError:
                translation = 'No translation for this segment'
            translations.append(translation)
            if(write_to_file):
                short_list = []
                short_list.append(translation)
                short_list = write_lines_to_file(sentence_filename + ".google_translate", short_list)
    return translations


def resume_translations(sentence_filename, partial_translation_file, sourceLang, targetLang="en", write_to_file=True):
    sentences = read_lines_from_file(sentence_filename)
    existing_translations = read_lines_from_file(partial_translation_file)
    translations = []
    for i, sentence in enumerate(sentences):
       translation = ''
       if i < len(existing_translations) and not existing_translations[i].startswith("No translation"):
          translation = existing_translations[i]
          print '.',
       else:
          try:
             translation = bingtrans.translate(sentence, sourceLang, targetLang)
             print '+',
          except ValueError:
             translation = 'No translation for this segment'
             print '-',
       if i % 100 == 0:
           print ' '
       translations.append(translation)
       if(write_to_file):
          short_list = []
          short_list.append(translation)
          short_list = write_lines_to_file(sentence_filename + ".google_translate", short_list)
    return translations


def generate_images_old_version(sentence_filename, output_dir, img_url_dir, fontName='Times New Roman'):
   """
   Saves image representations of the sentences to the output dir.
   The file name contains the article ID and the segment number.
   """
   sentences = read_lines_from_file(sentence_filename)
   seg_ids = read_lines_from_file(sentence_filename + '.seg_ids')
   img_urls = []
   width = 350
   extension = 'png'
   # create a placeholder file in case we have an odd number of segments
   dnt_filename = output_dir + '/do-not-translate.png'
   retval = str2img("Do not translate this sentence.", font=fontName, output=dnt_filename, width=width)
   # create images for all sentences
   for i, sentence in enumerate(sentences):
       seg_id = seg_ids[i]
       sentence = format_for_image(sentence)
       img_outputfile = '%s/%s.%s' % (output_dir, seg_id, extension)
       retval = str2img(sentence, font=fontName, output=img_outputfile, width=width)
       img_url = '%s/%s.%s' % (img_url_dir, seg_id, "png")
       img_urls.append(img_url)
   return img_urls


def generate_images(sentence_filename, output_dir, img_url_dir, fontName='Times New Roman'):
   """
   Saves image representations of the sentences to the output dir.
   The file name contains the article ID and the segment number.
   """
   os.system('java -cp /Users/ccb/Documents/Projects/wikitrans/ Str2ImgDemo %s %s %s "%s"' % (sentence_filename, sentence_filename + '.seg_ids', output_dir, fontName))
   img_urls = []
   # list the image URL paths for all sentences
   seg_ids = read_lines_from_file(sentence_filename + '.seg_ids')
   for i, seg_id in enumerate(seg_ids):
       img_url = '%s/%s.%s' % (img_url_dir, seg_id, "png")
       img_urls.append(img_url)
   return img_urls






def get_sentences_for_article(article, article_id, lang, sentence_filename, write_to_file=True):
   """
   Converts the article to text, splits it into sentences.  
   Appends the sentences to file
   """
   wikimarkup = wikipydia.query_text_raw(article, lang)['text']
   sentences,tags = wpTextExtractor.wiki2sentences(wikimarkup, determine_splitter(lang), True)
   if(write_to_file):
      sentences = write_lines_to_file(sentence_filename, sentences)
      tags = write_lines_to_file(sentence_filename + '.tags', tags)
      seg_ids = []
      for i in range(0, len(sentences)):
         id = article_id + '_' + str(i)
         seg_ids.append(id)
      seg_ids = write_lines_to_file(sentence_filename + '.seg_ids', seg_ids)
   return sentences


def filter_sentences(sentence_filename, lang, target_lang='en'):
    """
    Filter out sentences that are primrially English
    """
    sentences = read_lines_from_file(sentence_filename)
    p = re.compile(u'[a-zA-Z0-0 ]', re.VERBOSE)
    mask = []
    for i, sentence in enumerate(sentences):
        if not lang == 'en':
            excluding_ascii = p.sub(r'', sentence)
            punct = set(string.punctuation)
            excluding_ascii = ''.join(ch for ch in excluding_ascii if ch not in punct)
            no_spaces = sentence.replace(' ', '')
            if len(no_spaces) == 0:
                mask.append('0')
            elif (float(len(excluding_ascii)) / len(no_spaces)) > 0.5 and len(excluding_ascii) > 2:
                mask.append('1')
            else:
                mask.append('0')
        else:
            excluding_ascii = sentence         
            punct = set(string.punctuation)
            excluding_ascii = ''.join(ch for ch in excluding_ascii if ch not in punct)
            excluding_ascii = excluding_ascii.replace(' ', '')
            if len(excluding_ascii) > 2:
                mask.append('1')
            else:
                mask.append('0')
    mask = write_lines_to_file(sentence_filename + ".mask", mask)
    return mask



def format_for_image(string):
    """
    Cleans up the string so that it can be better rendered as an image.
    """
    string = string.replace("&nbsp;", " ")
    string = string.replace("&#160;", " ")
    # double quotes have to be converted to to two single quotes, 
    # because the image to string converter wraps the string in double quotes
    string = string.replace('"', "''")
    string = string.replace('`', "'")
    return string


def format_for_csv(string):
    """
    Replaces special characters used by comma separated value (CSV) files
    with their HTML equivalents.
    """
    string = string.strip()
    string = string.replace('\n', ' ')
    string = string.replace('&', "&amp;")
    string = string.replace(',', "&#44;")
    string = string.replace('>', "&gt;")
    string = string.replace('<', "&lt;")
    string = string.replace('"', "&quot;")
    string = string.replace("'", "&#39;")
    return string





def write_csv_file(csv_filename, sentence_filename, articles_filename, articles, lang, num_sentences_per_hit, img_output_dir, img_url_dir, fontName='Times New Roman', target_lang='en'):
   """
   Generates a comma seperated value file and associated image files 
   so that a Mechanical Turk translation HIT can be created.
   """
   init_files(sentence_filename, articles_filename)
   article_ids = []
   target_titles = []
   write_lines_to_file(articles_filename, articles)
   for article in articles:
       print article,
       article_id = wikipydia.query_page_id(article, language=lang)
       print article_id
       try:
           sentences = get_sentences_for_article(article, article_id, lang, sentence_filename)
           article_ids.append(article_id)
           ll = wikipydia.query_language_links(article, lang)
           if target_lang in ll:
               target_titles.append(ll[target_lang])
           else:
               target_titles.append('')
       except:
           target_titles.append('')
   write_lines_to_file(articles_filename + '.ids', article_ids)
   write_lines_to_file(articles_filename + '.target_titles', target_titles)
   #
   # translate all sentences
   translations = get_translations(sentence_filename, lang)
   #
   # generate all images
   img_urls = generate_images(sentence_filename, img_output_dir, img_url_dir, fontName)
   #
   # filter sentences that are mainly ascii
   mask = filter_sentences(sentence_filename, lang)
   #
   csv_output_file = open(csv_filename, 'w')
   header = 'lang_pair'
   for i in range(1, num_sentences_per_hit+1):
      header += ',seg_id%s' % str(i)
      header += ',tag%s' % str(i)
      header += ',seg%s' % str(i)
      header += ',img_url%s' % str(i)
      header += ',machine_translation%s' % str(i)
   #
   # load the sentences
   sentences = read_lines_from_file(sentence_filename)
   seg_ids = read_lines_from_file(sentence_filename + '.seg_ids')
   tags =  read_lines_from_file(sentence_filename + '.tags')
   mask =  read_lines_from_file(sentence_filename + '.mask')
   #
   line = header
   counter = 0
   for i, sentence in enumerate(sentences):
      if(mask[i] == '1'):
           if counter % num_sentences_per_hit == 0 :
               csv_output_file.write(line.encode('UTF-8'))
               csv_output_file.write('\n'.encode('UTF-8'))
               line = lang + "-" + target_lang               
           counter += 1
           seg_id = seg_ids[i]
           tag = tags[i]
           sentence = format_for_csv(sentence)
           img_url = img_urls[i]
           translation = format_for_csv(translations[i])
           line += ',%s,%s,%s,%s,%s' % (seg_id, tag, sentence, img_url, translation)
   # if there are an odd number of sentences, then fill out the rest of the fields with a do-not-translate message
   if not counter % num_sentences_per_hit == 0:
       dnt_url = ",,,," + img_url_dir + "/do-not-translate.png,"
       line = dnt_url * (num_sentences_per_hit - counter)
       csv_output_file.write(line.encode('UTF-8'))
   csv_output_file.write('\n'.encode('UTF-8'))
   csv_output_file.close()



def write_csv_file_from_files(csv_filename, sentence_filename, partial_translation_file,  articles_filename, articles, lang, num_sentences_per_hit, img_output_dir, img_url_dir, fontName='Times New Roman', target_lang='en'):
   """
   Generates a comma seperated value file and associated image files 
   so that a Mechanical Turk translation HIT can be created.
   """
   csv_output_file = open(csv_filename, 'w')
   header = 'lang'
   for i in range(1, num_sentences_per_hit+1):
      header += ',seg_id%s' % str(i)
      header += ',tag%s' % str(i)
      header += ',seg%s' % str(i)
      header += ',img_url%s' % str(i)
      header += ',machine_translation%s' % str(i)
   #
   # load the sentences
   seg_ids = read_lines_from_file(sentence_filename + '.seg_ids')
   tags =  read_lines_from_file(sentence_filename + '.tags')
   sentences = read_lines_from_file(sentence_filename)

   img_urls = []
   for i in range(0, len(sentences)):
       seg_id = seg_ids[i]
       img_url = '%s/%s.%s' % (img_url_dir, seg_id, "png")
       img_urls.append(img_url)
   #
   line = header
   counter = 0
   resume_translations(sentence_filename, partial_translation_file, lang)
   translations = read_lines_from_file(sentence_filename + '.google_translate')

   mask = filter_sentences(sentence_filename, lang)
#   mask =  read_lines_from_file(sentence_filename + '.mask')
   for i, sentence in enumerate(sentences):
      if(mask[i] == '1'):
           if counter % num_sentences_per_hit == 0 :
               csv_output_file.write(line.encode('UTF-8'))
               csv_output_file.write('\n'.encode('UTF-8'))
               line = lang + "-" + target_lang              
           counter += 1
           seg_id = seg_ids[i]
           tag = tags[i]
           sentence = format_for_csv(sentence)
           img_url = img_urls[i]
           translation = format_for_csv(translations[i])
           line += ',%s,%s,%s,%s,%s' % (seg_id, tag, sentence, img_url, translation)
   # if there are an odd number of sentences, then fill out the rest of the fields with a do-not-translate message
   if not counter % num_sentences_per_hit == 0:
       dnt_url = ",,,," + img_url_dir + "/do-not-translate.png,"
       line = dnt_url * (num_sentences_per_hit - counter)
       csv_output_file.write(line.encode('UTF-8'))
   csv_output_file.write('\n'.encode('UTF-8'))
   csv_output_file.close()




   
def extract_translations(dict_csv_file):
   reader = csv.reader(open(dict_csv_file), dialect=csv.excel)
   headers = {}
   translations_by_worker = {}
   worker_stats = {}
   for i, header in enumerate(reader.next()):
      headers[header] = i
   for row in reader:
      workerID = row[headers['WorkerId']]
      status = row[headers['AssignmentStatus']]
      if status == 'Approved':
         for i in range(1, 13):
            word = row[headers['Input.word_' + str(i)]].decode('utf8')
            translation = row[headers['Answer.translation_' + str(i) + '_1']].decode('utf8')
            if not word in translations_by_worker:
               translations_by_worker[word] = {}
            translations_by_worker[word][workerID] = translation
            if(i <=2):
               gold = row[headers['Input.translation_' + str(i)]].decode('utf8')
               try:
                   edit_distance = float(editdist.distance(gold.lower(), translation.lower())) / len(gold)
               except:
                   edit_distance = 1
               if not workerID in worker_stats:
                  worker_stats[workerID] = {}
                  worker_stats[workerID]['num_translations'] = 0
                  worker_stats[workerID]['total_edit_distance'] = 0
               worker_stats[workerID]['num_translations'] += 1   
               worker_stats[workerID]['total_edit_distance'] += edit_distance
   # calculate the performance of each worker 
   for workerID in worker_stats:
      num_translations = worker_stats[workerID]['num_translations']
      total_edit_distance = worker_stats[workerID]['total_edit_distance']
      avg_edit_distance = total_edit_distance / num_translations
      worker_stats[workerID]['avg_edit_distance'] = avg_edit_distance
   # extract the best translations
   best_translations = {}
   for word in translations_by_worker:
      best_translation = ''
      best_edit_distance = 1000
      for workerID in translations_by_worker[word]:
         if worker_stats[workerID]['avg_edit_distance'] <= best_edit_distance:
            best_translation = translations_by_worker[word][workerID]
            best_edit_distance = worker_stats[workerID]['avg_edit_distance']
      if best_translation != '':
         best_translation = best_translation.replace(' ', '_')
         best_translations[word] = best_translation
   print len(best_translations.keys())
   return best_translations

   

def gloss_sentences(sentences, translations):
   glosses = []
   for sentence in sentences:
      gloss = ''
      words = sentence.split(' ')
      for word in words:
         if word in translations:
            gloss = gloss + translations[word] + ' '
         else:
            gloss = gloss + word + ' '
      glosses.append(gloss)
   return glosses



def determine_splitter(language):
   LANGUAGE_CHOICES = {
       'en':'English',
       'ur':'Urdu',
       'es':'Spanish',
       'de':'German',
       'fr':'French',
       'cs':'Czech',
       'ko':'Korean',
       'hi':'Hindi',
       'ja':'Japanese',
       }
   if language == 'ur':
      return urdu_split_sentences
   elif language == 'ar':
      return determine_splitter('ur')
   elif language == 'fa':
      return determine_splitter('ur')
   elif language == 'hi':
      return hindi_split_sentences
   elif language == 'ja':
      return japanese_split_sentences
   elif language == 'ko':
      return determine_splitter('en')
   elif language == 'ta':
      return determine_splitter('en')
   elif language == 'te':
      return determine_splitter('en')
   elif language == 'ml':
      return determine_splitter('en')
   tokenizer = 'tokenizers/punkt/%s.pickle' % (LANGUAGE_CHOICES[language].lower())
   try:
      tokenizer = nltk.data.load(tokenizer)
      return tokenizer.tokenize
   except:
      return determine_splitter('en')

def split_sentences(text, split_after, split_before=''):
   """
   Split text into sentences after the specified patterns, optionally 
   before other characters like BULLET, and at multiple newlines.
   """
   # break on multiple newline characters
   multiple_newlines = re.compile('\s*\n+\n+|\n+\s+\n+')
   text = multiple_newlines.sub('MULTIPLENEWLINESPLACEHOLDER', text)  
   # trim initial whitespace
   initial_whitespace = re.compile('^\s+')
   text = initial_whitespace.sub('', text)   
   # replace multiple whitespaces (including single newlines) with space
   whitespace = re.compile('\s+')
   text = whitespace.sub(' ', text)
   # do lang-specific splitting
   if not split_after == '':
      p = re.compile(split_after, re.VERBOSE)
      text = p.sub(r'\1\n', text)
   if not split_before == '':
      p = re.compile(split_before, re.VERBOSE)
      text = p.sub(r'\n\1', text)
   # restore the multiple newline placeholder
   multiple_newlines_placeholder = re.compile('MULTIPLENEWLINESPLACEHOLDER')
   text = multiple_newlines_placeholder.sub('\n', text)
   text = multiple_newlines.sub('\n', text)   
   # filter out blank lines and return
   sentences = []
   for sentence in text.split('\n'):
      sentence = sentence.strip()
      if not sentence == '':
         sentences.append(sentence) 
   return sentences 


def urdu_split_sentences(text):
   DASH = u'\u06D4' # arabic full stop
   QUESTION = u'\u061F'
   ELLIPSIS = u'\u2026'
   FULL_STOP = u'\u002e'
   BULLET = u'\u2022'
 
   split_after = u'([%s|%s|%s|%s])' % (QUESTION, ELLIPSIS, FULL_STOP, DASH)
   split_before = u'([%s])' % (BULLET)
   return split_sentences(text, split_after, split_before)


def hindi_split_sentences(text):
   """
   This method duplicates the Urdu sentence splitter except for 
   Hindi-specific sentence boundary characters.  We should decompose the
   two function definition so that code is shared.
   """
   EXCLAMATION = u'!'
   QUESTION = u'?'
   ELLIPSIS = u'\u2026'
   FULL_STOP = u'\u0964' # hindi full stop
   BULLET = u'\u2022'
 
   split_after = u'([%s|%s|%s|%s])' % (QUESTION, ELLIPSIS, FULL_STOP, EXCLAMATION)
   split_before = u'([%s])' % (BULLET)
   return split_sentences(text, split_after, split_before)


def japanese_split_sentences(text):
   FULL_STOP = u'\u3002'
   ELLISIS_1 = u'\u2026'
   ELLISIS_2 = u'\u2025'
   EXCLAMATION_1 = u'\u0021'
   EXCLAMATION_2 = u'\u01C3'
   DOUBLE_EXCLAMATION = u'\u203C'
   QUESTION_1 = u'\u003F'
   QUESTION_2 = u'\uFF1F'
   DOUBLE_QUESTION = u'\u2047'
   BULLET = u'\u2022'
   PART_ALTERNATION_MARK = u'\u303D'
   split_after = u'([%s|%s|%s|%s|%s|%s|%s|%s|%s])' % (FULL_STOP, ELLISIS_1, ELLISIS_2, EXCLAMATION_1, EXCLAMATION_2, DOUBLE_EXCLAMATION, QUESTION_1, QUESTION_2, DOUBLE_QUESTION)
   split_before = u'([%s|%s])' % (BULLET, PART_ALTERNATION_MARK)
   return split_sentences(text, split_after, split_before)


lang = 'ja'
target_lang = 'en'
fontName='Times New Roman'
start_doc = 0
end_doc = 100
set_label = 'japanese_wikipedia_treding_topics_from_March_16'
freq_view_filename = '/Users/ccb/Documents/Projects/wikitrans/ja/wikitopics-2011-03-16'


articles = []
lines = read_lines_from_file(freq_view_filename)
articles = lines[0:25]
#for line in lines[0:25]:
#    unquoted = urllib.unquote(line.encode('ascii'))
#    try:
#        articles.append(unquoted.decode('utf8'))
#    except UnicodeDecodeError:
#        print 'Skipping ', unquoted

articles = articles[start_doc:end_doc]
#date_time_str = time.strftime("%Y-%m-%dT%H%M")
date_time_str = '2011-04-03T1054'
path = '/Users/ccb/Documents/Projects/wikitrans/%s/%s/' % (lang, date_time_str)

img_output_dir = path + 'txt_img'
img_url_dir = 'http://cs.jhu.edu/~ccb/wikitrans/%s/%s/txt_img' % (lang, date_time_str)
start_doc +=1
csv_filename = path + set_label + "-" + date_time_str + ".%s-%s.csv" % (start_doc, end_doc)
sentence_filename = path + lang + '_sentences'
articles_filename = path + lang + '_articles'
num_sentences_per_hit = 10

if not os.path.exists(path):
    os.makedirs(path)

if not os.path.exists(img_output_dir):
    os.makedirs(img_output_dir)

#generate_images(sentence_filename, img_output_dir, img_url_dir)
generate_images_old_version(sentence_filename, img_output_dir, img_url_dir, fontName='Osaka')
    
partial_translation_file = '/Users/ccb/Documents/Projects/wikitrans/ja/2011-04-03T1054/ja_sentences.google_translate.partial'

#write_csv_file(csv_filename, sentence_filename, articles_filename, articles, lang, num_sentences_per_hit, img_output_dir, img_url_dir, fontName, target_lang)
write_csv_file_from_files(csv_filename, sentence_filename, partial_translation_file, articles_filename, articles, lang, num_sentences_per_hit, img_output_dir, img_url_dir, fontName='TimesNewRoman', target_lang='en')
