package org.contexity.qcg.sentenceanalyzer.rest;

import java.util.List;

import org.contexity.qcg.sentenceanalyzer.dto.SentenceAnalysisResult;
import org.contexity.qcg.sentenceanalyzer.service.SentenceAnalysisService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Web controller for the sentence analysis service.
 * 
 * @author Contexity
 */
@RestController
@RequestMapping("/api")
public class SentenceAnalysisController {

	private final SentenceAnalysisService sentenceAnalysisService;

	public SentenceAnalysisController(SentenceAnalysisService sentenceAnalysisService) {
		this.sentenceAnalysisService = sentenceAnalysisService;
	}

	/**
	 * {@code GET  /analyze-text} : get all the customers.
	 *
	 * @return the {@link ResponseEntity} with status {@code 200 (OK)} and the list
	 *         of customers in body.
	 */
	@GetMapping("/analyze-text")
	public List<SentenceAnalysisResult> analyzeSentence(@RequestParam(name = "text", required = true) String text) {
		return sentenceAnalysisService.analyze(text);
	}

}
