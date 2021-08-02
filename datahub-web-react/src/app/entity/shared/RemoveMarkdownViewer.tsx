import React from 'react';
import { Typography } from 'antd';
import removeMd from 'remove-markdown';
import styled from 'styled-components';

const RemoveMarkdownContainer = styled.div`
    display: block;
    overflow-wrap: break-word;
    word-wrap: break-word;
    overflow-x: hidden;
    overflow-y: auto;
`;

const DescriptionParagraph = styled(Typography.Paragraph)`
    &&& {
        margin-bottom: 0px;
    }
`;

export type Props = {
    source: string;
    limit?: number;
};

export default function RemoveMarkdownViewer({ source, limit = 1000 }: Props) {
    const plainText = removeMd(source, {
        stripListLeaders: true,
        gfm: true,
        useImgAltText: true,
    })
        .replace(/\n\s*\n/g, '•') // replace linebreaks with •
        .replace(/^•/, '') // remove first •
        .substring(0, limit);

    return (
        <RemoveMarkdownContainer>
            <DescriptionParagraph>{plainText}</DescriptionParagraph>
        </RemoveMarkdownContainer>
    );
}
