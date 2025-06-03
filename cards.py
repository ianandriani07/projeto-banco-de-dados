import textwrap
import wcwidth
from typing import List, Tuple, Optional


class PrintableCard: ...


def get_visual_size(text: str) -> int:
    return wcwidth.wcswidth(text)


def separate_printable_cards(
    components: List[str | Tuple[str] | PrintableCard],
) -> List[List[str] | PrintableCard]:
    output = []
    current_stacked_components = []

    for component in components:
        if isinstance(component, PrintableCard):
            if current_stacked_components:
                output.append(current_stacked_components)
            output.append(component)
            current_stacked_components = []
        else:
            current_stacked_components.append(component)

    if current_stacked_components:
        output.append(current_stacked_components)

    return output


def format_card(
    data_list: List[str | Tuple[str]],
    inner_card_width: int = 44,
    padding_char: str = " ",
    add_top: bool = True,
    add_bottom: bool = True,
) -> List[str]:
    """
    Formats a list of strings and tuples into a text-based profile card.

    Args:
        data_list (list): A list of items to format.
            - String: Will be displayed on one or more lines.
                All lines derived from a string item (initial, from newline,
                or from wrapping) will be prefixed with a single space.
                Newlines ('\\n') in the string create new lines in the card.
                Long lines are wrapped.
            - Tuple of strings: Elements are joined by "   " (three spaces)
                and displayed on a single line. This line is
                NOT prefixed with an extra space automatically.
                It's assumed to fit `inner_card_width`;
                if longer, it will be truncated by the padding.
        inner_card_width (int): The width of the content area between the vertical borders.
        padding_char (str): The character used for padding lines to `inner_card_width`.
            Should not be an emoji or wide character.
    """
    borders = {
        "tl": "╔",
        "tr": "╗",
        "bl": "╚",
        "br": "╝",
        "h": "═",
        "v": "║",
        "ml": "╠",
        "mr": "╣",
    }

    if not isinstance(inner_card_width, int) or inner_card_width <= 0:
        raise ValueError("inner_card_width must be a positive integer.")
    if not isinstance(padding_char, str) or len(padding_char) != 1:
        raise ValueError("padding_char must be a single character string.")

    output_lines = []

    # Top border
    if add_top:
        output_lines.append(
            borders["tl"] + borders["h"] * inner_card_width + borders["tr"]
        )

    # TextWrapper for string items.
    # The indent takes 1 char, so text content width is inner_card_width - 1.
    # TextWrapper itself uses len() for width, not visual width. This is a known
    # limitation if strings have many wide chars and are near wrapping length.
    # For this example, it should be fine.
    string_wrapper = textwrap.TextWrapper(
        width=inner_card_width - 1,  # Width for the text content itself
        initial_indent=" ",  # Prepended to the first line of a wrapped segment
        subsequent_indent=" ",  # Prepended to subsequent lines of a wrapped segment
        break_long_words=True,
        break_on_hyphens=True,
        replace_whitespace=False,
        drop_whitespace=True,  # Strips whitespace from line_segment before indenting
    )

    for i, item in enumerate(data_list):
        current_item_processed_lines = []

        if isinstance(item, str):
            # Strings are processed by splitting by '\n' first.
            # Each segment is then wrapped with consistent indentation.
            original_lines = item.split("\n")
            for line_segment in original_lines:
                wrapped_segments = string_wrapper.wrap(line_segment)
                if (
                    not wrapped_segments
                ):  # Handles empty line_segment or segment becoming empty after drop_whitespace
                    current_item_processed_lines.append(" ")  # Add just the indent
                else:
                    current_item_processed_lines.extend(wrapped_segments)

        elif isinstance(item, tuple):
            tuple_content_string = "   ".join(str(s) for s in item)
            if tuple_content_string:
                tuple_content_string = " " + tuple_content_string

            current_item_processed_lines.append(
                tuple_content_string
            )  # No auto-indent for tuples

        elif item is None:
            current_item_processed_lines.append(
                " "
            )  # None treated as an indented empty line

        else:  # Catch-all for other data types
            # Convert to string, then treat like a single-line string item (gets indented and wrapped)
            line_segment = str(item)
            wrapped_segments = string_wrapper.wrap(line_segment)
            if not wrapped_segments:
                current_item_processed_lines.append(" ")
            else:
                current_item_processed_lines.extend(wrapped_segments)

        # Format these processed lines (pad and add vertical borders)
        for text_segment in current_item_processed_lines:
            visual_len = get_visual_size(text_segment)
            padding_needed = inner_card_width - visual_len
            if padding_needed < 0:
                padding_needed = 0  # Avoid negative padding if content is too wide

            padded_content = text_segment + (padding_char * padding_needed)
            output_lines.append(f"{borders['v']}{padded_content}{borders['v']}")

        # Add separator line if not the last item in data_list
        if i < len(data_list) - 1:
            output_lines.append(
                borders["ml"] + borders["h"] * inner_card_width + borders["mr"]
            )

    # Bottom border
    if add_bottom:
        output_lines.append(
            borders["bl"] + borders["h"] * inner_card_width + borders["br"]
        )

    return output_lines


def pad_lines(
    seq: List[str],
    desired_seq_length: Optional[int] = None,
    desired_element_length: Optional[int] = None,
    pad_char: str = " ",
):
    pad_lines = desired_element_length is not None
    if not pad_lines:
        if not seq:
            raise ValueError(
                "If elements_desired_length is not set you cannot pass an empty sequence!"
            )

        desired_element_length = len(seq[0])

    new_seq = []
    if pad_lines:
        for el in seq:
            if len(el) >= desired_element_length:
                new_seq.append(el)
                continue

            new_seq.append(el + pad_char * (desired_element_length - len(el)))
    else:
        new_seq = seq

    if desired_seq_length is None:
        return new_seq

    if len(new_seq) >= desired_seq_length:
        return new_seq

    padding_string = pad_char * desired_element_length
    new_seq.extend([padding_string for _ in range(desired_seq_length - len(new_seq))])

    return new_seq


class PrintableCard:

    def __init__(
        self,
        *card_elements: str | Tuple[str],
        inner_card_width: int = 44,
        padding_char: str = " ",
    ):
        """Creates a card.
        Args:
            data_list (list): A list of items to format.
                - String: Will be displayed on one or more lines.
                    All lines derived from a string item (initial, from newline,
                    or from wrapping) will be prefixed with a single space.
                    Newlines ('\\n') in the string create new lines in the card.
                    Long lines are wrapped.
                - Tuple of strings: Elements are joined by "   " (three spaces)
                    and displayed on a single line. This line is
                    NOT prefixed with an extra space automatically.
                    It's assumed to fit `inner_card_width`;
                    if longer, it will be truncated by the padding.
            inner_card_width (int): The width of the content area between the vertical borders.
            padding_char (str): The character used for padding lines to `inner_card_width`.
                Should not be an emoji or wide character.
        """
        self.components = separate_printable_cards(card_elements)
        self._inner_card_width = inner_card_width
        self.padding_char = padding_char

    @property
    def inner_card_width(self):
        return self._inner_card_width

    def get_lines(self, add_top, add_bottom) -> List[str]: ...

    def __repr__(self):
        return "\n".join(self.get_lines())


class Card(PrintableCard):

    def __init__(
        self,
        *card_elements: str | Tuple[str] | PrintableCard,
        inner_card_width: int = 44,
        padding_char: str = " ",
    ):
        super().__init__(
            *card_elements, inner_card_width=inner_card_width, padding_char=padding_char
        )

    def get_lines(self, add_top: bool = True, add_bottom: bool = True) -> List[str]:
        if not self.components:
            return []

        output_lines = []

        for component in self.components:
            if isinstance(component, PrintableCard):
                lines = component.get_lines(add_top=True, add_bottom=True)
                if lines:
                    if output_lines:
                        lines_length: int = len(lines[0])
                        output_lines_length: int = len(output_lines[0])

                        max_length = max(lines_length, output_lines_length)

                        output_lines = pad_lines(
                            output_lines, desired_element_length=max_length
                        )
                        lines_length = pad_lines(
                            lines, desired_element_length=max_length
                        )

                    output_lines.extend(lines)
            else:
                output_lines.extend(
                    format_card(
                        component,
                        self.inner_card_width,
                        self.padding_char,
                        add_top=True,
                        add_bottom=True,
                    )
                )

        if not add_top and output_lines:
            output_lines = output_lines[1:]

        if not add_bottom and output_lines:
            output_lines = output_lines[:-1]

        return output_lines


Vertical = Card


class Horizontal(PrintableCard):

    def __init__(
        self,
        *card_elements: str | Tuple[str] | PrintableCard,
        inner_card_width: int = 44,
        padding_char: str = " ",
        horizontal_stack_width: int = 88,
    ):
        super().__init__(
            *card_elements, inner_card_width=inner_card_width, padding_char=padding_char
        )
        self.horizontal_stack_width = horizontal_stack_width

    def stack_horizontally(self, formatted_components: List[List[str]]):
        if not formatted_components:
            return []

        output: List[str] = formatted_components[0]

        for comp in formatted_components[1:]:
            len_output = len(output)
            len_comp = len(comp)

            # if (
            #     output
            #     and comp
            #     and len(output[0]) + len(comp[0]) > self.horizontal_stack_width
            # ):
            #     max_length = max(len(comp[0]), len(output[0]))

            #     output = pad_lines(output, desired_element_length=max_length)
            #     comp = pad_lines(comp, desired_element_length=max_length)

            #     output.extend(comp)
            #     continue

            max_length = max(len_output, len_comp)

            output = pad_lines(output, desired_seq_length=max_length)
            comp = pad_lines(comp, desired_seq_length=max_length)

            for i in range(max_length):
                output[i] = output[i] + comp[i]

        return output

    def get_lines(self, add_top: bool = True, add_bottom: bool = True) -> List[str]:
        if not self.components:
            return []

        formatted_components = []

        for component in self.components:
            if isinstance(component, PrintableCard):
                lines = component.get_lines(add_top=True, add_bottom=True)
                if lines:
                    formatted_components.append(lines)
            else:
                formatted_components.append(
                    format_card(
                        component,
                        self.inner_card_width,
                        self.padding_char,
                        add_top=True,
                        add_bottom=True,
                    )
                )

        output_lines = self.stack_horizontally(formatted_components)

        if not add_top and output_lines:
            output_lines = output_lines[1:]

        if not add_bottom and output_lines:
            output_lines = output_lines[:-1]

        return output_lines


class Sep(PrintableCard):

    def __init__(self):
        pass

    def get_lines(self, add_top: bool = True, add_bottom: bool = True) -> List[str]:
        return []


if __name__ == "__main__":

    print(
        Horizontal(
            Vertical(
                Horizontal("Hello", Card("World", inner_card_width=12)),
                Horizontal("Fuck", Sep(), "You"),
            ),
            "Test",
            "World",
        )
    )
