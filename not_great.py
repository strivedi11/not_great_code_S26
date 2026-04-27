import json

import matplotlib.pyplot as plt
import pandas as pd


def load_modcloth_data(path='modcloth_small_data.json'):
    """Load line-delimited JSON into a DataFrame."""
    with open(path, encoding='utf8') as infile:
        records = [json.loads(line) for line in infile]
    return pd.DataFrame(records)


def height_converter(height_str):
    """Convert a height string like '5ft 7in' to inches."""
    if pd.isna(height_str):
        return height_str

    split_height = height_str.split('ft')
    height_in_inches = int(split_height[0]) * 12
    if len(split_height) == 2 and split_height[1] != '':
        height_in_inches += int(split_height[1].split('in')[0])
    return height_in_inches


def build_color_trend_by_year():
    """Build a year-indexed table of distinct color counts."""
    sets_df = pd.read_csv('sets.csv')
    colors_df = pd.read_csv('colors.csv')
    inventories_df = pd.read_csv('inventories.csv')
    inventory_parts_df = pd.read_csv('inventory_parts.csv')

    parts_with_colors = inventory_parts_df.merge(
        colors_df,
        left_on='color_id',
        right_on='id',
        how='inner',
    )
    parts_with_inventory = parts_with_colors.merge(
        inventories_df,
        left_on='inventory_id',
        right_on='id',
        how='inner',
    )
    merged_df = parts_with_inventory.merge(
        sets_df,
        on='set_num',
        how='inner',
    )

    return pd.pivot_table(
        data=merged_df,
        values='rgb',
        index='year',
        aggfunc='nunique',
    )


def main():
    modcloth_data = load_modcloth_data()
    modcloth_data['height'] = modcloth_data['height'].apply(height_converter)

    color_trend = build_color_trend_by_year()
    plt.plot(color_trend)
    plt.axvline(x=2004, c='r')
    plt.ylabel('unique colors per year')


if __name__ == '__main__':
    main()
