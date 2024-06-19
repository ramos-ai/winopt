#!/bin/bash
# Usage:
#   evaluate_all_languages.sh <corpus> <output-folder>
set -e

corpus_fn=$1
out_folder=$2


# langs=("ar" "uk" "he" "ru" "it" "fr" "es" "de" "pt")
langs=("pt")
mt_systems=("sota" "aws" "bing" "google" "model_b" "model_cbs" "padrao-mbart-finetuned-news_commentary" "padrao-mbart-finetuned-opus_books" "padrao-unicamp-finetuned-news_commentary" "padrao-unicamp-finetuned-opus_books" "padrao-unicamp-finetuned-opus_books" "padrao-unicamp-vanessa-finetuned-handscrafted" "pt-unicamp-handcrafted" "pt-unicamp-handcrafted-puro" "systran" "unicamp-dl-translation-en-pt-t5")
# mt_systems=("model_cbs")


# Make sure systran has all translations
# for lang in ${langs[@]}
# do
#     echo "Translating $lang with systran..."
#     ../scripts/systran_language.sh $corpus_fn $lang
# done

for trans_sys in ${mt_systems[@]}
do
    for lang in ${langs[@]}
    do
        echo "evaluating $trans_sys, $lang"
        if [[ "$lang" == "uk" && "$trans_sys" == "aws" ]]; then
            echo "skipping.."
            continue
        fi

        if [[ "$trans_sys" == "sota" ]]; then
            if [[ "$lang" != "de" && "$lang" != "fr" ]]; then
                echo "skipping.."
                continue
            fi
        fi

        if [[ "$trans_sys" == "unicamp_news" ]]; then
            if [[ "$lang" != "pt" ]]; then
                echo "skipping.."
                continue
            fi
        fi

        if [[ "$trans_sys" == "unicamp_handcrafted" ]]; then
            if [[ "$lang" != "pt" ]]; then
                echo "skipping.."
                continue
            fi
        fi

        if [[ "$trans_sys" == "model_cbs" ]]; then
            if [[ "$lang" != "pt" ]]; then
                echo "skipping.."
                continue
            fi
        fi


        # Run evaluation
        mkdir -p $out_folder/$trans_sys
        out_file=$out_folder/$trans_sys/$lang.log
        echo "Evaluating $lang into $out_file"
        ../scripts/evaluate_language.sh $corpus_fn $lang $trans_sys > $out_file
    done
done

echo "DONE!"
