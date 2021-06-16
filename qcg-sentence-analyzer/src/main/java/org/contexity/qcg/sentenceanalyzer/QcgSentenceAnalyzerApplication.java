package org.contexity.qcg.sentenceanalyzer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

/**
 * Main application class for the sentence analyzer service.
 *  
 * @author Contexity
 */
@SpringBootApplication
@ComponentScan
public class QcgSentenceAnalyzerApplication {

	public static void main(String[] args) {
		SpringApplication.run(QcgSentenceAnalyzerApplication.class, args);
	}

}
