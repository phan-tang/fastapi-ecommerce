export interface IconLink {
    name: string;
    iconLink: string;
    link?: string;
    title?: string;
    badge?: number;
}

export interface DropdownItems {
    buttonDisplay: IconLink;
    options: DropdownItem[];
}

export interface DropdownItem {
    title: string;
    name: string;
    id: string;
    iconLink: string;

}