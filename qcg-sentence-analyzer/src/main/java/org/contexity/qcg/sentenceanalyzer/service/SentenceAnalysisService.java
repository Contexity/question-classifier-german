package org.contexity.qcg.sentenceanalyzer.service;

import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import org.contexity.qcg.sentenceanalyzer.dto.SentenceAnalysisResult;
import org.springframework.stereotype.Service;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.IndexedWord;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.semgrex.SemgrexMatcher;
import edu.stanford.nlp.semgraph.semgrex.SemgrexPattern;
import edu.stanford.nlp.trees.ud.CoNLLUDocumentReader;
import edu.stanford.nlp.util.Pair;

/**
 * Main analysis service that determines whether a piece of text --split into
 * sentences-- contains question words or phrases indicative of question syntax.
 * 
 * @author Contexity
 */
@Service
public class SentenceAnalysisService {

	/**
	 * The words / word combinations considered question words if they occur in
	 * analyzed text
	 */
	private static Set<String> QUESTION_WORDS_GERMAN = new HashSet<>(
			Arrays.asList("gibt es", "mit wem", "seit wann", "wann", "warum", "weshalb", "weswegen", "wieso", "was",
					"welche", "welchen", "welchem", "welcher", "welches", "wem", "wen", "wer", "wessen", "wie",
					"wieweit", "wie viel", "wie lange", "wie viel", "wie viele", "wo", "wogegen", "wodurch", "wofür",
					"wozu", "womit", "wodurch", "worum", "worüber", "wobei", "wovon", "woraus", "wohin", "wohinter",
					"woher", "womit", "woran", "worin", "worauf", "worunter", "wovor", "woneben", "worüber"));

	/**
	 * A "semantic regular expression" pattern for identifying verbs and verb-like
	 * words in a semantic graph, and their corresponding subjects.
	 * 
	 * The patterns means: find words with a POS tag starting with 'V', that have a
	 * "subject" ('sb') relation to another (group of) word(s), along with the (root
	 * of the) word (group).
	 */
	private static SemgrexPattern VERB_WITH_SUBJECT_PATTERN = SemgrexPattern.compile("{pos:/V.*/}=verb >sb {}=subject");

	/** Service used to analyze text and get the resulting CoNLL-U table */
	private final ConlluService conlluService;

	/** Instance of reader for parsing CoNLL-U tables */
	private final CoNLLUDocumentReader documentReader;

	/**
	 * Creates a new instance of the SentenceAnalysisService
	 * 
	 * @param conlluService the service used to analyze text and get the resulting
	 *                      CoNLL-U table
	 */
	public SentenceAnalysisService(ConlluService conlluService) {
		this.conlluService = conlluService;
		documentReader = new CoNLLUDocumentReader();
	}

	/**
	 * The entry point for the analysis. The steps performed here are:
	 * <ul>
	 * <li>the provided text is sent to the {@link #conlluService CoNLL-U analysis
	 * service}</li>
	 * <li>the CoNLL-U table(s) received are parsed into {@link SemanticGraph
	 * semantic graphs}</li>
	 * <li>the text is analyzed for the presence of question words</li>
	 * <li>the semantic graphs are analyzed for the presence of phrases with
	 * question syntax</li>
	 * </ul>
	 * 
	 * @param text the text to be analyzed
	 * @return the results of the analysis encapsulated in
	 *         {@link SentenceAnalysisResult result objects}, one for each sentence
	 *         in the original text
	 */
	public List<SentenceAnalysisResult> analyze(String text) {
		if (text == null || text.trim().isEmpty())
			return Collections.emptyList();

		final List<SentenceAnalysisResult> analysisResults = new ArrayList<>();

		try {
			String cleanText = text.trim().replaceAll("\\s+", " ");
			String conllu = conlluService.getConlluForTool(cleanText);
			if (conllu == null || conllu.trim().isEmpty())
				return Collections.emptyList();

			// get the semantic graphs and create the results
			Iterator<Pair<SemanticGraph, SemanticGraph>> isg = documentReader.getIterator(new StringReader(conllu));
			while (isg.hasNext()) {
				Pair<SemanticGraph, SemanticGraph> sgpair = isg.next();
				SemanticGraph sg = sgpair.first;
				SentenceAnalysisResult sar = new SentenceAnalysisResult(sg.toRecoveredSentenceString(), sg);
				analyzeQuestionWords(sar);
				analyzeQuestionSyntax(sar);
				analysisResults.add(sar);
			}
		} catch (Exception e) {
			System.err.println("Error while processing text: " + text);
			e.printStackTrace(System.err);
			analysisResults.add(new SentenceAnalysisResult(text, null));
		}

		return analysisResults;
	}

	/**
	 * Analyzes the provided text to determine if it contains any known question
	 * words.
	 * 
	 * @param sar The analysis result which serves as both input (text to analyze)
	 *            and output (identified words if any) object
	 */
	private void analyzeQuestionWords(SentenceAnalysisResult sar) {
		String sentence = sar.getSemanticGraph().toRecoveredSentenceString().toLowerCase();
		for (String qw : QUESTION_WORDS_GERMAN) {
			if (sentence.contains(qw))
				sar.addQuestionWord(qw);
		}
	}

	/**
	 * Analyzes the provided text to determine if it contains any question syntax.
	 * The current implementation is rather simplistic, looking for verbs (or
	 * equivalent) that precede their subjects.
	 * 
	 * @param sar The analysis result which serves as both input (text to analyze)
	 *            and output (identified phrases with question syntax if any) object
	 */
	private void analyzeQuestionSyntax(SentenceAnalysisResult sar) {
		SemanticGraph sg = sar.getSemanticGraph();
		SemgrexMatcher matcher = VERB_WITH_SUBJECT_PATTERN.matcher(sg, true);
		if (matcher.find()) {
			IndexedWord subject = matcher.getNode("subject");
			IndexedWord verb = matcher.getNode("verb");
			if (verb.index() < subject.index()) {
				String verbText = verb.get(CoreAnnotations.TextAnnotation.class);
				String subjectText = subject.get(CoreAnnotations.TextAnnotation.class);
				sar.addQuestionPhrase(verb.index() + ". " + verbText + " -> " + subject.index() + ". " + subjectText);
			}
		}
	}

}
