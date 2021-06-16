package org.contexity.qcg.sentenceanalyzer.service;

import java.util.List;

import org.contexity.qcg.sentenceanalyzer.dto.SentenceAnalysisResult;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SentenceAnalysisServiceTest {

	@Autowired
	private SentenceAnalysisService sentenceAnalysisService;
	
	@Test
	void testAnalyze() {
		List<SentenceAnalysisResult> results = sentenceAnalysisService.analyze("Funkioniert das denn?");
		System.out.println(results);
		results = sentenceAnalysisService.analyze("Und wer?");
		System.out.println(results);
		results = sentenceAnalysisService.analyze("Und ist es?");
		System.out.println(results);
	}

}
