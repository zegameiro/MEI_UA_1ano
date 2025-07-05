#include "utf-8.h"

int utf8_decode(UTF8DecoderState &state, uint16_t byte, uint32_t *codepoint) {
  if (state.remaining_bytes > 0) {
    state.codepoint = (state.codepoint << 6) | (byte & 0x3F);
    state.remaining_bytes--;

    if (state.remaining_bytes == 0) {
      *codepoint = state.codepoint;
      return state.number_bytes;
    }
    return 0;
  }

  if ((byte & 0x80) == 0x00) {
    state.codepoint = byte;
    *codepoint = state.codepoint;
    return 1;
  } else if ((byte & 0xE0) == 0xC0) {
    state.remaining_bytes = 1;
    state.number_bytes = 2;
    state.codepoint = byte & 0x1F;
  } else if ((byte & 0xF0) == 0xE0) {
    state.remaining_bytes = 2;
    state.number_bytes = 3;
    state.codepoint = byte & 0x0F;
  } else if ((byte & 0xF8) == 0xF0) {
    state.remaining_bytes = 3;
    state.number_bytes = 4;
    state.codepoint = byte & 0x07;
  } else {
    return -1;
  }
  return 0;
}

bool utf8_is_letter(uint32_t codepoint) {
  switch (codepoint) {
  case 0x41 ... 0x5A:
  case 0x61 ... 0x7A:
  case 0xC0 ... 0xFF:
  case 0x100 ... 0x17F:
  case 0x180 ... 0x24F:
  case 0x250 ... 0x2AF:
  case 0x370 ... 0x3FF:
  case 0x400 ... 0x4FF:
  case 0x500 ... 0x52F:
  case 0x2100 ... 0x214F:
  case 0x4E00 ... 0x9FFF:
    return true;
    break;
  default:
    return false;
    break;
  }
}

bool utf8_is_space(uint32_t codepoint) {
  switch (codepoint) {
  case 0x0009:
  case 0x000A:
  case 0x000B:
  case 0x000C:
  case 0x000D:
  case 0x0020:
  case 0x00A0:
  case 0x2007:
  case 0x202F:
  case 0x2060:
    return true;
    break;

  default:
    return false;
    break;
  }
}