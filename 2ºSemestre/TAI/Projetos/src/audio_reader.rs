use hound::WavReader;
use rustfft::{FftPlanner, num_complex::Complex};
use std::collections::HashMap;

pub fn extract_dominant_frequencies(
    wav_path: &str, 
    segment_ms: u32, 
    top_n: usize,
    start_ms: Option<u32>,
    end_ms: Option<u32>
) -> HashMap<String ,Vec<Vec<f32>>> {
    let mut reader = WavReader::open(wav_path).expect("ERROR: Unable to open WAV file");
    let spec = reader.spec();
    let sample_rate = spec.sample_rate;
    let all_samples: Vec<f32> = reader.samples::<i16>()
        .map(|s| s.unwrap() as f32)
        .collect();
    
    let start_sample = (spec.sample_rate as f32 * start_ms.unwrap_or(0) as f32 / 1000.0) as usize;
    let end_sample = (spec.sample_rate as f32 * end_ms.unwrap_or(0) as f32 / 1000.0) as usize;

    if end_sample > all_samples.len() {
        panic!("ERROR: End time exceeds the length of the audio file");
    }

    let samples: &[f32];

    if (start_ms.is_none() && end_ms.is_none()) || (start_ms == Some(0) && end_ms == Some(0)) {
        samples = &all_samples;
    }  else {
        println!("Processing sample {} from {} ms to {} ms", wav_path, start_ms.unwrap_or(0), end_ms.unwrap_or(0));
        samples = &all_samples[start_sample..end_sample];
    }

    // Calculate the number of samples per segment
    let samples_per_segment = (sample_rate as f32 * segment_ms as f32 / 1000.0) as usize;
    let hop_size = samples_per_segment / 2; // Overlap by 50%

    let mut dominant_freqs_per_segment = vec![];
    let mut least_dominant_freqs_per_segment = vec![];

    let mut planner = FftPlanner::new();
    let fft = planner.plan_fft_forward(samples_per_segment);

    for start in (0..samples.len() - samples_per_segment).step_by(hop_size) {
        let window: Vec<Complex<f32>> = samples[start..start + samples_per_segment]
            .iter()
            .map(|&s| Complex::new(s, 0.0))
            .collect();

        let mut buffer = window.clone();
        fft.process(&mut buffer);

        let magnitudes: Vec<f32> = buffer.iter().map(|c| c.norm()).collect();
        let mut indexed: Vec<(usize, f32)> = magnitudes.iter().cloned().enumerate().collect();
        indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        let freqs = indexed.iter()
            .take(top_n)
            .map(|&(i, _)| (i as f32 * sample_rate as f32 / samples_per_segment as f32))
            .collect::<Vec<f32>>();

        dominant_freqs_per_segment.push(freqs);

        let least_freqs = indexed.iter()
            .rev()
            .take(top_n)
            .map(|&(i, _)| (i as f32 * sample_rate as f32 / samples_per_segment as f32))
            .collect::<Vec<f32>>();
        least_dominant_freqs_per_segment.push(least_freqs);
    }

    let mut result = HashMap::new();
    result.insert("dominant".to_string(), dominant_freqs_per_segment);
    result.insert("least_dominant".to_string(), least_dominant_freqs_per_segment);

    result
}