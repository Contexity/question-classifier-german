package org.contexity.qcg.sentenceanalyzer.dto;

import java.util.LinkedList;
import java.util.List;

import org.contexity.qcg.sentenceanalyzer.rest.SentenceAnalysisController;
import org.contexity.qcg.sentenceanalyzer.service.SentenceAnalysisService;

import edu.stanford.nlp.semgraph.SemanticGraph;

/**
 * Data transfer object used in the API responses for
 * {@link SentenceAnalysisController#analyzeSentence(String)}. The most
 * important members are {@link #getContainsQuestionWords()
 * containsQuestionWords} and {@link #getContainsQuestionSyntax()
 * containsQuestionSyntax}.
 * 
 * Note tha this is only a data transfer object, for the actual logic please see
 * {@link SentenceAnalysisService}
 * 
 * @author Contexity
 */
public class SentenceAnalysisResult {

	/** The actual text analyzed - typically a stand-alone sentence */
	private String text = "";
	/** The semantic graph of the text */
	private SemanticGraph semanticGraph = null;
	/**
	 * Whether the text contains question words - see
	 * {@link SentenceAnalysisService} for the words themselves.
	 */
	private boolean containsQuestionWords = false;
	/** The question words identified in the text */
	private List<String> questionWords = null;
	/**
	 * Whether the syntax of the text indicates a question - see
	 * {@link SentenceAnalysisService} for the logic.
	 */
	private boolean containsQuestionSyntax = false;
	/**
	 * The (parts of) phrases in the text that are indicative of question syntax.
	 */
	private List<String> questionPhrases = null;

	/**
	 * Creates a new SentenceAnalysisResult
	 * 
	 * @param text          The text that was analyzed
	 * @param semanticGraph The semantic graph of the analyzed text
	 */
	public SentenceAnalysisResult(String text, SemanticGraph semanticGraph) {
		this(text, semanticGraph, null, null);
	}

	/**
	 * Creates a new SentenceAnalysisResult
	 * 
	 * @param text            The text that was analyzed
	 * @param semanticGraph   The semantic graph of the analyzed text
	 * @param questionWords   The question words identified in the text
	 * @param questionPhrases The phrases indicative of question syntax identified
	 *                        in the text
	 */
	public SentenceAnalysisResult(String text, SemanticGraph semanticGraph, List<String> questionWords,
			List<String> questionPhrases) {
		this.text = text;
		this.semanticGraph = semanticGraph;

		if (questionWords != null && !questionWords.isEmpty()) {
			this.containsQuestionWords = true;
			this.questionWords = questionWords;
		}
		if (questionPhrases != null && !questionPhrases.isEmpty()) {
			this.containsQuestionSyntax = true;
			this.questionPhrases = questionPhrases;
		}
	}

	/**
	 * Adds a question word to those identified in the analyzed text
	 * 
	 * @param word The new word
	 * @return {@code true} if the word is successfully added, {@code false}
	 *         otherwise
	 */
	public boolean addQuestionWord(String word) {
		if (word != null && !word.trim().isEmpty()) {
			if (questionWords == null)
				questionWords = new LinkedList<>();
			containsQuestionWords = true;
			return questionWords.add(word);
		}
		return false;
	}

	/**
	 * Adds a phrase indicative of question syntax to those identified in the
	 * analyzed text
	 * 
	 * @param word The new phrase
	 * @return {@code true} if the phrase is successfully added, {@code false}
	 *         otherwise
	 */
	public boolean addQuestionPhrase(String phrase) {
		if (phrase != null && !phrase.trim().isEmpty()) {
			if (questionPhrases == null)
				questionPhrases = new LinkedList<>();
			containsQuestionSyntax = true;
			return questionPhrases.add(phrase);
		}
		return false;
	}

	/**
	 * Retrieves the analyzed text
	 * 
	 * @return the analyzed text
	 */
	public String getText() {
		return text;
	}

	/**
	 * Retrieves flag indicating presence of question words in the analyzed text
	 * 
	 * @return {@code true} if the text contains any question words, {@code false}
	 *         otherwise
	 */
	public boolean getContainsQuestionWords() {
		return containsQuestionWords;
	}

	/**
	 * Retrieves the question words in the analyzed text, if any
	 * 
	 * @return the question words
	 */
	public List<String> getQuestionWords() {
		return questionWords;
	}

	/**
	 * Retrieves flag indicating presence of phrases with question syntax in the
	 * analyzed text
	 * 
	 * @return {@code true} if the text contains any question syntax, {@code false}
	 *         otherwise
	 */
	public boolean getContainsQuestionSyntax() {
		return containsQuestionSyntax;
	}

	/**
	 * Retrieves the phrases with question syntax in the analyzed text, if any
	 * 
	 * @return the question words
	 */
	public List<String> getQuestionPhrases() {
		return questionPhrases;
	}

	/**
	 * Retrieves the semantic graph of the analyzed text - may be {@code null} if
	 * the analysis could not be completed successfully
	 * 
	 * @return the semantic graph of the analyzed text
	 */
	public SemanticGraph getSemanticGraph() {
		return semanticGraph;
	}

	@Override
	public String toString() {
		return "SentenceAnalysisResult [text=" + text + ", containsQuestionWords=" + containsQuestionWords
				+ ", questionWords=" + questionWords + ", containsQuestionSyntax=" + containsQuestionSyntax
				+ ", questionPhrases=" + questionPhrases + ", semanticGraph=" + semanticGraph + "]";
	}

}
