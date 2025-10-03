#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cctype>
#include <sstream>
#include <iostream>

struct SentimentScore {
    double positive;
    double negative;
    double neutral;
    
    SentimentScore() : positive(0.0), negative(0.0), neutral(1.0) {}
};

class PerceptionModule {
private:
    std::map<std::string, double> positive_keywords;
    std::map<std::string, double> negative_keywords;
    
public:
    PerceptionModule() {
        positive_keywords["good"] = 0.8;
        positive_keywords["great"] = 0.9;
        positive_keywords["excellent"] = 0.95;
        positive_keywords["happy"] = 0.85;
        positive_keywords["love"] = 0.9;
        positive_keywords["wonderful"] = 0.9;
        positive_keywords["amazing"] = 0.95;
        positive_keywords["perfect"] = 0.9;
        
        negative_keywords["bad"] = 0.8;
        negative_keywords["terrible"] = 0.9;
        negative_keywords["awful"] = 0.9;
        negative_keywords["hate"] = 0.9;
        negative_keywords["sad"] = 0.7;
        negative_keywords["poor"] = 0.7;
        negative_keywords["worst"] = 0.95;
        negative_keywords["horrible"] = 0.9;
    }
    
    std::string to_lowercase(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(),
                      [](unsigned char c){ return std::tolower(c); });
        return result;
    }
    
    std::vector<std::string> tokenize(const std::string& text) {
        std::vector<std::string> tokens;
        std::istringstream iss(text);
        std::string word;
        
        while (iss >> word) {
            std::string clean_word;
            for (char c : word) {
                if (std::isalnum(c)) {
                    clean_word += c;
                }
            }
            if (!clean_word.empty()) {
                tokens.push_back(to_lowercase(clean_word));
            }
        }
        
        return tokens;
    }
    
    SentimentScore analyze_sentiment(const std::string& text) {
        SentimentScore score;
        std::vector<std::string> words = tokenize(text);
        
        double positive_sum = 0.0;
        double negative_sum = 0.0;
        int positive_count = 0;
        int negative_count = 0;
        
        for (const auto& word : words) {
            auto pos_it = positive_keywords.find(word);
            if (pos_it != positive_keywords.end()) {
                positive_sum += pos_it->second;
                positive_count++;
            }
            
            auto neg_it = negative_keywords.find(word);
            if (neg_it != negative_keywords.end()) {
                negative_sum += neg_it->second;
                negative_count++;
            }
        }
        
        if (positive_count > 0 || negative_count > 0) {
            double total = positive_sum + negative_sum;
            if (total > 0) {
                score.positive = positive_sum / total;
                score.negative = negative_sum / total;
                score.neutral = 0.0;
            }
        }
        
        return score;
    }
    
    std::map<std::string, int> extract_keywords(const std::string& text, int min_length = 4) {
        std::map<std::string, int> keyword_freq;
        std::vector<std::string> words = tokenize(text);
        
        for (const auto& word : words) {
            if (word.length() >= static_cast<size_t>(min_length)) {
                keyword_freq[word]++;
            }
        }
        
        return keyword_freq;
    }
};

extern "C" {
    PerceptionModule* perception_create() {
        return new PerceptionModule();
    }
    
    void perception_destroy(PerceptionModule* module) {
        delete module;
    }
    
    void perception_analyze(PerceptionModule* module, const char* text,
                           double* positive, double* negative, double* neutral) {
        SentimentScore score = module->analyze_sentiment(std::string(text));
        *positive = score.positive;
        *negative = score.negative;
        *neutral = score.neutral;
    }
}
