package org.contexity.qcg.sentenceanalyzer.service;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

/**
 * A simple service that performs a call to a service GET endpoint that receives
 * text to analyze and returns a CoNLL-U table. This service just encapsulates
 * the call, it does not do any validation of results received.
 * 
 * @author Contexity
 */
@Service
public class ConlluService {

	/** Class-specific logger */
	private static final Logger LOG = LoggerFactory.getLogger(ConlluService.class);

	/** The name of cache in which cached results from service calls are saved */
	public static final String CONLLUSERVICE_CACHE = "conllu";

	/**
	 * The URL to call the service by. It's assumed the string contains a '%s' where
	 * the actual text to be analyzed is written in URL-encoded format.
	 */
	private final String serviceURL;

	public ConlluService(@Value("${services.conllu.url}") String serviceURL) {
		this.serviceURL = serviceURL;
	}

	/**
	 * Performs a GET request to the service's endpoint after adding the URL-encoded
	 * version of {@code text} to the URL.
	 * 
	 * @param text The text to analyze
	 * 
	 * @return The CoNLL-U table returned from the serivce, or an empty string if
	 *         the call wasn't successful.
	 */
	@Cacheable(CONLLUSERVICE_CACHE)
	public String getConlluForTool(String text) {

		// get the conllu table(s) for the text
		String conllu = "";
		URL toolURL = null;
		try {
			toolURL = new URL(String.format(serviceURL, URLEncoder.encode(text, StandardCharsets.UTF_8.name())));
			Object content = toolURL.getContent();
			if (content instanceof InputStream) {
				conllu = IOUtils.toString((InputStream) content, StandardCharsets.UTF_8);
				try {
					((InputStream) content).close();
				} catch (Exception e) {
					LOG.warn("Error while closing intput stream for: {}", toolURL, e);
				}
				return conllu;
			}

		} catch (MalformedURLException | UnsupportedEncodingException e) {
			LOG.error("URL or protocol error while attempting to call '{}' for text '{}' using '{}'", toolURL, text, e);
		} catch (IOException e) {
			LOG.error("Error while attempting to call '{}' for phrase '{}' ", toolURL, text, e);
		}

		return conllu;
	}
}
